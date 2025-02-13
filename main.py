import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from bot_key import bot_key,sheet_id

# Thêm logging ở đầu file, sau phần import
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Các trạng thái cho conversation handler
INPUT_NAME, CHOOSE_DATE, CONFIRM_DAYOFF, INPUT_SUBSTITUTE = range(4)

# Thiết lập Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = sheet_id
RANGE_NAME = "'Trang tính1'!A2:H"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Xem lịch dạy", callback_data='check_calen'),
            InlineKeyboardButton("Báo nghỉ", callback_data='request_day_off')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Xin chào! Tôi là bot quản lý lịch dạy.\n"
        "Tôi có thể giúp bạn:\n"
        "✅ Xem lịch dạy của giáo viên\n"
        "✅ Báo nghỉ và sắp xếp giáo viên dạy thay\n\n"
        "Vui lòng chọn chức năng bên dưới:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('session_'):
        row_index = int(query.data.split('_')[1])
        context.user_data['row_index'] = row_index
        
        # Lấy thông tin ca dạy từ sheet
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'Trang tính1'!A{row_index}:D{row_index}"
        ).execute()
        row = result.get('values', [])[0]
        
        await query.message.reply_text(
            f"Xác nhận nghỉ ngày {context.user_data['selected_date']}?\n"
            f"Ca: {row[1]}\n"
            f"Môn: {row[2]}\n"
            f"Lớp: {row[3]}\n"
            "Gõ 'ok' để xác nhận hoặc bất kỳ để hủy"
        )
        return CONFIRM_DAYOFF
    elif query.data == 'check_calen':
        await query.message.reply_text("Vui lòng nhập tên của bạn để xem lịch dạy:")
        context.user_data['action'] = 'check_calendar'
        return INPUT_NAME
    elif query.data == 'request_day_off':
        if 'teacher_name' not in context.user_data:
            await query.message.reply_text("Vui lòng nhập tên của bạn trước:")
            context.user_data['action'] = 'request_dayoff'
            return INPUT_NAME
        else:
            await query.message.reply_text(
                f"Xin chào {context.user_data['teacher_name']}, "
                "vui lòng nhập ngày muốn nghỉ (định dạng DD/MM/YYYY):"
            )
            return CHOOSE_DATE
    elif query.data == 'want_dayoff':
        if 'teacher_name' not in context.user_data:
            await query.message.reply_text("Vui lòng nhập tên của bạn trước:")
            context.user_data['action'] = 'request_dayoff'
            return INPUT_NAME
        else:
            await query.message.reply_text(
                f"Xin chào {context.user_data['teacher_name']}, "
                "vui lòng nhập ngày muốn nghỉ (định dạng DD/MM/YYYY):"
            )
            return CHOOSE_DATE
    elif query.data == 'no_dayoff':
        await query.message.reply_text("Cảm ơn bạn đã xem lịch dạy!")
        return ConversationHandler.END

async def input_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teacher_name = update.message.text
    context.user_data['teacher_name'] = teacher_name
    
    if context.user_data.get('action') == 'check_calendar':
        await check_calen(update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            f"Xin chào {teacher_name}, "
            "vui lòng nhập ngày muốn nghỉ (định dạng DD/MM/YYYY):"
        )
        return CHOOSE_DATE

async def check_calen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teacher_name = context.user_data.get('teacher_name')
    try:
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        values = result.get('values', [])
        
        if not values:
            await update.message.reply_text('Không có dữ liệu')
            return ConversationHandler.END

        response = f"📅 Lịch dạy của giáo viên {teacher_name}:\n\n"
        found = False
        for row in values:
            if row[5] == teacher_name:
                found = True
                response += f"📌 Ngày: {row[0]}\n"
                response += f"⏰ Ca: {row[1]}\n"
                response += f"📚 Môn: {row[2]}\n"
                response += f"👥 Lớp: {row[3]}\n"
                response += f"🏫 Phòng: {row[4]}\n"
                response += f"📝 Trạng thái: {row[6]}\n"
                if len(row) > 7 and row[7]:
                    response += f"GV thay: {row[7]}\n"
                response += "---------------\n"
        
        if not found:
            await update.message.reply_text(f"Không tìm thấy lịch dạy của giáo viên {teacher_name}")
            return ConversationHandler.END

        await update.message.reply_text(response)
        
        # Thêm câu hỏi về việc báo nghỉ
        keyboard = [
            [
                InlineKeyboardButton("Có", callback_data='want_dayoff'),
                InlineKeyboardButton("Không", callback_data='no_dayoff')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Bạn có muốn báo nghỉ không?",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
        
    except Exception as e:
        await update.message.reply_text(f"Có lỗi xảy ra: {str(e)}")
        return ConversationHandler.END

async def process_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_date = update.message.text
    teacher_name = context.user_data.get('teacher_name')
    
    # Tìm dòng tương ứng trong sheet
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    values = result.get('values', [])
    
    # Tìm tất cả các ca dạy trong ngày được chọn
    teaching_sessions = []
    for i, row in enumerate(values):
        if row[0] == selected_date and row[5] == teacher_name:
            teaching_sessions.append({
                'index': i + 2,  # +2 vì dòng đầu là header
                'ca': row[1],
                'mon': row[2],
                'lop': row[3]
            })
    
    if not teaching_sessions:
        await update.message.reply_text(
            f"Không tìm thấy lịch dạy của bạn vào ngày {selected_date}!"
        )
        return ConversationHandler.END
    
    if len(teaching_sessions) == 1:
        # Nếu chỉ có 1 ca dạy
        session = teaching_sessions[0]
        context.user_data['row_index'] = session['index']
        await update.message.reply_text(
            f"Xác nhận nghỉ ngày {selected_date}?\n"
            f"Ca: {session['ca']}\n"
            f"Môn: {session['mon']}\n"
            f"Lớp: {session['lop']}\n"
            "Gõ 'ok' để xác nhận hoặc bất kỳ để hủy"
        )
        return CONFIRM_DAYOFF
    else:
        # Nếu có nhiều ca dạy
        keyboard = []
        for session in teaching_sessions:
            button_text = f"Ca {session['ca']} - {session['mon']} - {session['lop']}"
            keyboard.append([InlineKeyboardButton(
                button_text, 
                callback_data=f"session_{session['index']}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data['selected_date'] = selected_date
        
        await update.message.reply_text(
            "Bạn có nhiều ca dạy trong ngày này.\n"
            "Vui lòng chọn ca muốn báo nghỉ:",
            reply_markup=reply_markup
        )
        return CONFIRM_DAYOFF

async def confirm_dayoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.lower()
    if response == 'ok':
        # Cập nhật trạng thái
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'Trang tính1'!G{context.user_data['row_index']}",
            valueInputOption='RAW',
            body={'values': [['Báo nghỉ']]}
        ).execute()
        
        await update.message.reply_text("Đã cập nhật trạng thái báo nghỉ thành công!")
        await update.message.reply_text("Vui lòng nhập tên giáo viên dạy thay:")
        return INPUT_SUBSTITUTE
    else:
        await update.message.reply_text("Đã hủy yêu cầu nghỉ.")
        # Hiển thị menu chính
        keyboard = [
            [
                InlineKeyboardButton("Xem lịch dạy", callback_data='check_calen'),
                InlineKeyboardButton("Báo nghỉ", callback_data='request_day_off')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Bạn muốn làm gì tiếp theo?",
            reply_markup=reply_markup
        )
        return ConversationHandler.END

async def input_substitute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    substitute_name = update.message.text
    
    # Cập nhật tên giáo viên dạy thay
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'Trang tính1'!H{context.user_data['row_index']}",
        valueInputOption='RAW',
        body={'values': [[substitute_name]]}
    ).execute()
    
    await update.message.reply_text(f"Đã cập nhật giáo viên dạy thay: {substitute_name}")
    
    # Hiển thị menu chính
    keyboard = [
        [
            InlineKeyboardButton("Xem lịch dạy", callback_data='check_calen'),
            InlineKeyboardButton("Báo nghỉ", callback_data='request_day_off')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Bạn muốn làm gì tiếp theo?",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

def main():
    logger.info("Bot đang khởi động...")
    application = ApplicationBuilder().token(bot_key).build()
    
    # Thêm handlers
    application.add_handler(CommandHandler("start", start))
    
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_handler),
            CommandHandler('check_calen', lambda u, c: input_name(u, c)),
            CommandHandler('request_day_off', lambda u, c: input_name(u, c))
        ],
        states={
            INPUT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_name)],
            CHOOSE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_date)],
            CONFIRM_DAYOFF: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_dayoff)],
            INPUT_SUBSTITUTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_substitute)]
        },
        fallbacks=[CallbackQueryHandler(button_handler)]
    )
    application.add_handler(conv_handler)
    
    logger.info("Bot đã sẵn sàng!")
    application.run_polling()

if __name__ == '__main__':
    main()
