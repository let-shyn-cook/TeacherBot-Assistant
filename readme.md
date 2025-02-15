<div align="center">
  <h1>
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=40&pause=1000&color=3498DB&center=true&vCenter=true&random=false&width=500&lines=Telegram+Bot+Qu%E1%BA%A3n+L%C3%BD;L%E1%BB%8Bch+D%E1%BA%A1y+Gi%C3%A1o+Vi%C3%AAn" alt="Typing SVG" />
  </h1>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/Telegram-Bot-blue.svg" alt="Telegram">
    <img src="https://img.shields.io/badge/Google-Sheets-green.svg" alt="Google Sheets">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  </p>

  <p align="center">
    <a href="#tính-năng-chính">Tính năng</a> •
    <a href="#cài-đặt">Cài đặt</a> •
    <a href="#cấu-hình">Cấu hình</a> •
    <a href="#sử-dụng">Sử dụng</a> •
    <a href="#đóng-góp">Đóng góp</a>
  </p>
</div>

## 📝 Mô tả

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

Bot Telegram giúp quản lý lịch dạy của giáo viên, cho phép xem lịch và báo nghỉ một cách dễ dàng. Dữ liệu được đồng bộ với Google Sheets.

## ⭐ Tính năng chính

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

- 📅 Xem lịch dạy cá nhân
- 🔔 Báo nghỉ dạy
- 👥 Đăng ký giáo viên dạy thay
- 📊 Tích hợp với Google Sheets
- 🔄 Cập nhật realtime

## 🔧 Cài đặt

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

```
git clone https://github.com/your-username/teacher-schedule-bot.git

cd teacher-schedule-bot

pip install -r requirements.txt
```

## ⚙️ Cấu hình

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

1. Tạo bot Telegram qua [@BotFather](https://t.me/botfather)
2. Tạo project Google Cloud và bật Google Sheets API
3. Tạo service account và tải file credentials.json
4. Cập nhật `bot_key.py`:
```python
bot_key = "YOUR_BOT_TOKEN"
sheet_id = "YOUR_SHEET_ID"
```

## 🔄 Luồng Hoạt Động Chi Tiết

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

### 1. Khởi động Bot
- Gửi lệnh `/start` 
- Bot hiển thị menu với 2 lựa chọn:
  + Xem lịch dạy
  + Báo nghỉ

### 2. Xem lịch dạy
1. Chọn "Xem lịch dạy"
2. Nhập tên giáo viên
3. Bot hiển thị thông tin:
   - Ngày
   - Ca dạy
   - Môn học
   - Lớp
   - Phòng
   - Trạng thái
   - GV dạy thay (nếu có)
4. Bot hỏi "Bạn có muốn báo nghỉ không?"
   - Nếu chọn "Có" -> Chuyển sang luồng báo nghỉ
   - Nếu chọn "Không" -> Kết thúc

### 3. Báo nghỉ
1. Chọn "Báo nghỉ" hoặc "Có" từ xem lịch
2. Nếu chưa có tên:
   - Nhập tên giáo viên
3. Nhập ngày muốn nghỉ (DD/MM/YYYY)
4. Bot kiểm tra lịch dạy:
   - Nếu không có -> Thông báo và kết thúc
   - Nếu có 1 ca -> Hiển thị thông tin và yêu cầu xác nhận
   - Nếu có nhiều ca -> Hiển thị danh sách để chọn
5. Xác nhận nghỉ:
   - Gõ "ok" để xác nhận
   - Gõ bất kỳ để hủy
6. Nếu xác nhận:
   - Nhập tên giáo viên dạy thay
   - Bot cập nhật Google Sheets:
     + Trạng thái: "Báo nghỉ"
     + GV dạy thay: [Tên GV mới]
7. Hiển thị menu chính

```mermaid
flowchart TB
    subgraph Left["Luồng Chính"]
        direction TB
        subgraph Menu["Menu Chính"]
            A[Người dùng] --> B{/start}
            B --> C[Xem lịch dạy]
            B --> D[Báo nghỉ]
        end

        subgraph Actions["Hành Động"]
            G --> |1 ca| H[Xác nhận]
            G --> |Nhiều ca| I[Chọn ca]
            I --> H
            H --> |ok| J[Nhập GV thay]
            J --> K[Cập nhật sheets]
            K --> B
        end
    end

    subgraph Process["Xử Lý"]
        direction TB
        C --> C1[Nhập tên GV]
        D --> E[Nhập tên GV]
        C1 --> C2[Hiển thị lịch]
        E --> F[Nhập ngày nghỉ]
        C2 --> C3{Muốn báo nghỉ?}
        F --> G{Kiểm tra lịch}
    end

    C3 --> |Có| F
    C3 --> |Không| Z[Kết thúc]
    G --> |Không có| Z
    H --> |hủy| Z
```
## 📚 Cấu Trúc Dữ Liệu

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

| Cột | Mô tả |
|-----|--------|
| A | Ngày |
| B | Ca dạy |
| C | Môn học |
| D | Lớp |
| E | Phòng |
| F | Giáo viên |
| G | Trạng thái |
| H | GV dạy thay |

## 🚀 Sử dụng

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

1. Khởi động bot:
```bash
python main.py
```

2. Tương tác với bot qua Telegram:
- `/start` - Bắt đầu
- Chọn "Xem lịch dạy" hoặc "Báo nghỉ"
- Làm theo hướng dẫn của bot

## 🤝 Đóng góp

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

1. Fork project
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

<div align="center">
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>

MIT License - Xem [LICENSE](LICENSE) để biết thêm chi tiết

---
<div align="center">
  Made with ❤️ by Shyn
  <img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%">
</div>
