# Changelog

Mọi thay đổi đáng chú ý của dự án được ghi lại tại đây.
Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
tuân thủ [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]

### Fixed
- **dx-portal:** form ticket báo nhầm "Không kết nối được DX-Core" dù đã gửi thành công.
  Nguyên nhân: `e.currentTarget` bị null sau `await` (React), khiến `reset()` ném lỗi
  và rơi vào nhánh catch. Sửa: lưu tham chiếu form trước `await`. Đã kiểm chứng bằng
  trình duyệt thật (Chrome headless): ticket hợp lệ hiện khung xanh, SĐT sai hiện Poka-yoke.

## [0.3.0] - 2026-07-03

### Added
- **[H] DX-Portal (G2)** — cổng thông tin nội bộ (Next.js 14, tự viết): trang chủ
  "nguồn sự thật duy nhất" gom nghiệp vụ + dashboard + công cụ; form gửi ticket
  (proxy an toàn tới DX-Core, hiện thông điệp Poka-yoke thân thiện).
- Luồng DX-Ticket khép kín, bấm được: Form → DX-Core → PostgreSQL → Metabase.
- **[D] Metabase Dashboard (G2)** — BI đọc dữ liệu ticket từ PostgreSQL (SSOT):
  dashboard "DX-Ticket" với 7 biểu đồ (tổng ticket, quá hạn SLA, tỷ lệ hoàn thành,
  theo loại/trạng thái/ưu tiên, xu hướng theo ngày).
- Script `scripts/metabase_setup.py` tự động cấu hình Metabase (admin, kết nối DB, dashboard).
- Dữ liệu mẫu `seed/seed_tickets.sql` (40 ticket đa dạng, phân bố đều).
- Service `metabase` + init DB `metabase` trong docker-compose.
- **DX-Core (G1)** — trục trung gian hướng sự kiện (FastAPI): tiếp nhận ticket qua
  webhook, rào chắn Poka-yoke (xác thực SĐT), rule engine (suy luận ưu tiên, phân công,
  tính SLA), ghi PostgreSQL (SSOT), cảnh báo Telegram.
- 11 unit test cho rule engine + Poka-yoke (pass).
- Dockerfile cho dx-core; thêm service `dx-core` và `baserow` vào docker-compose.
- Khởi tạo nền móng dự án (Giai đoạn G0): cây thư mục, bộ tài liệu nguồn mở.
- Giấy phép MIT + `.gitignore`, `.dockerignore`, `.env.example`.
- Tài liệu định hướng dự án `docs/du-an.md` và bộ giáo trình DX-OS trong `docs/dx-os/`.

## [0.1.0] - 2026-07-03

### Added
- Bản khởi tạo kho mã nguồn công khai (scaffold).
