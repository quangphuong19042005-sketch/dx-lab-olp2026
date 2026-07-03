# DX-Core — Trục trung gian hướng sự kiện

Thành phần **nguyên gốc** của DX-Lab OSS (giấy phép MIT). Đóng vai trò *"trục trung gian
hướng sự kiện"* mà giáo trình DX-OS chương 6.3 yêu cầu: khâu nối [P] Process với [D] Data
và [H] Human.

## Luồng xử lý

```
Biểu mẫu Baserow [P]  ──webhook──▶  DX-Core
                                     │  1. Chuẩn hóa + Poka-yoke (chặn SĐT sai)
                                     │  2. Rule engine: suy luận ưu tiên, phân công, tính SLA
                                     │  3. Ghi PostgreSQL [D] (nguồn sự thật)
                                     └▶ 4. Cảnh báo Telegram [H]
```

## API

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/health` | Kiểm tra sống |
| POST | `/webhooks/ticket` | Tiếp nhận ticket mới (JSON `TicketIn`) |

Ví dụ:

```bash
curl -X POST http://localhost:8000/webhooks/ticket -H 'Content-Type: application/json' -d '{
  "title": "Máy lạnh không chạy",
  "customer_name": "Nguyễn Văn A",
  "customer_phone": "0901234567",
  "category": "ky_thuat"
}'
```

## Chạy & kiểm thử

```bash
pip install -e ".[dev]"     # cài kèm công cụ test
pytest                      # chạy unit test (rule engine, không cần DB)
uvicorn app.main:app --reload
```

Hoặc qua Docker (trong `docker compose` toàn hệ thống): service `dx-core`.
