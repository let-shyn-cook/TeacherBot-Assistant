import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Thiết lập Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1FTItLCPJ7HlV11HJj0W6F5kpitMFxTgoQNnO9yTauRc'
RANGE_NAME = "'Trang tính1'!A2:H"

# Dữ liệu mẫu
sample_data = [
    # Giáo viên A - dạy cả tuần
    ["15/03/2024", "Sáng", "Toán", "10A1", "P201", "Nguyễn Văn A", "Bình thường", ""],
    ["16/03/2024", "Sáng", "Toán", "11A1", "P201", "Nguyễn Văn A", "Bình thường", ""],
    ["17/03/2024", "Chiều", "Toán", "12A1", "P201", "Nguyễn Văn A", "Bình thường", ""],
    ["18/03/2024", "Sáng", "Toán", "10A2", "P201", "Nguyễn Văn A", "Bình thường", ""],
    ["19/03/2024", "Chiều", "Toán", "11A2", "P201", "Nguyễn Văn A", "Bình thường", ""],
    
    # Các giáo viên khác - mỗi người 2 tiết
    ["15/03/2024", "Chiều", "Lý", "11A2", "P202", "Trần Thị B", "Bình thường", ""],
    ["17/03/2024", "Sáng", "Lý", "12A2", "P202", "Trần Thị B", "Bình thường", ""],
    
    ["16/03/2024", "Sáng", "Hóa", "12A3", "P203", "Phạm Văn C", "Bình thường", ""],
    ["18/03/2024", "Chiều", "Hóa", "11A3", "P203", "Phạm Văn C", "Bình thường", ""],
    
    ["15/03/2024", "Sáng", "Sinh", "10A2", "P204", "Lê Thị D", "Bình thường", ""],
    ["17/03/2024", "Chiều", "Sinh", "12A2", "P204", "Lê Thị D", "Bình thường", ""],
    
    ["16/03/2024", "Chiều", "Văn", "11A1", "P205", "Hoàng Văn E", "Bình thường", ""],
    ["19/03/2024", "Sáng", "Văn", "10A3", "P205", "Hoàng Văn E", "Bình thường", ""],
    
    ["15/03/2024", "Chiều", "Anh", "12A1", "P206", "Ngô Thị F", "Bình thường", ""],
    ["18/03/2024", "Sáng", "Anh", "11A1", "P206", "Ngô Thị F", "Bình thường", ""],
    
    ["16/03/2024", "Sáng", "Sử", "10A3", "P207", "Đỗ Văn G", "Bình thường", ""],
    ["19/03/2024", "Chiều", "Sử", "12A3", "P207", "Đỗ Văn G", "Bình thường", ""],
    
    ["17/03/2024", "Sáng", "Địa", "11A3", "P208", "Bùi Thị H", "Bình thường", ""],
    ["19/03/2024", "Chiều", "Địa", "10A1", "P208", "Bùi Thị H", "Bình thường", ""],
    
    ["18/03/2024", "Chiều", "GDCD", "12A2", "P209", "Vũ Văn I", "Bình thường", ""],
    ["19/03/2024", "Sáng", "GDCD", "11A2", "P209", "Vũ Văn I", "Bình thường", ""],
    
    ["15/03/2024", "Sáng", "Tin", "10A1", "P210", "Đinh Thị K", "Bình thường", ""],
    ["17/03/2024", "Chiều", "Tin", "12A1", "P210", "Đinh Thị K", "Bình thường", ""]
]

def add_sample_data():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Xóa dữ liệu cũ (nếu có)
        clear_request = sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        )
        clear_request.execute()

        # Thêm dữ liệu mới
        request = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body={'values': sample_data}
        )
        response = request.execute()
        print("Đã thêm dữ liệu mẫu thành công!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")

if __name__ == '__main__':
    add_sample_data() 