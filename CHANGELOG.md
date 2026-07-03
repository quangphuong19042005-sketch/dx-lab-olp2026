# Changelog

Mọi thay đổi đáng chú ý của dự án được ghi lại tại đây.
Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
tuân thủ [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]

### Added
- **Dữ liệu mở liên kết [D]** (kế thừa OLP 2025) — DX-Core xuất ticket ra JSON-LD
  (`@context` ánh xạ schema.org), CSV, và danh mục DCAT (W3C); **ẩn PII** (tên/SĐT).
  Endpoint `/open-data/*`; lược đồ `schemas/ticket.schema.json` + `schemas/dx-context.jsonld`
  + ví dụ `examples/tickets.jsonld`; thẻ "Cổng Dữ liệu mở" trong DX-Portal.

### Security
- **Backend chỉ bind loopback** (`127.0.0.1`) cho postgres/qdrant/dx-core/dx-rag — không
  còn phơi API ghi dữ liệu & AI (không auth) ra LAN. Portal vẫn gọi qua docker network.
- **Bảo vệ API proxy bằng session**: `/api/tickets`, `/api/assistant` trả 401 nếu chưa
  đăng nhập (đóng lỗ "SSO chỉ chặn UI"; chống lạm dụng quota AI).
- `metabase_setup.py` không còn hardcode/không in mật khẩu — bắt buộc lấy từ env.

### Fixed
- **dx-rag chống crash khi demo**: bọc try/except mọi call LLM/Qdrant trong `/ask`
  (mạng/quota/timeout → thông báo mềm thay vì 500); xử lý Gemini trả `candidates` rỗng
  (safety filter); `search` trả rỗng khi collection chưa tồn tại.
- **dx-rag re-ingest** tạo lại collection → không sót tri thức lỗi thời.
- **dx-core** escape HTML các trường người dùng trong cảnh báo Telegram (tránh vỡ parse);
  `send_alert` best-effort tuyệt đối (không làm 500 sau khi ticket đã lưu).

### Added
- **Tài liệu kiến trúc** `docs/kien-truc.md`: sơ đồ Mermaid (kiến trúc H-P-D-I, luồng
  DX-Ticket, luồng SSO), bảng dịch vụ/cổng/giấy phép, và 5 ảnh màn hình demo thật.

## [0.5.0] - 2026-07-03

### Added
- **SSO thật (OIDC) cho DX-Portal ↔ Keycloak** [H]: bảo vệ toàn bộ trang qua middleware,
  đăng nhập một lần, hiển thị người dùng + đăng xuất. Dùng next-auth (MIT).
- Giải bài toán mạng Docker: cố định issuer `localhost:8080` + backchannel động để
  container gọi token qua `keycloak:8080`. Kiểm chứng luồng đăng nhập đầy đủ bằng Chrome headless.
- Tự động nạp tri thức dx-rag khi khởi động nếu kho trống.

## [0.4.0] - 2026-07-03

### Added
- **DX-RAG — Trợ lý AI nội bộ chống ảo giác [I]** (FastAPI): RAG bám tài liệu SOP,
  hỗ trợ 2 backend (Gemini API mặc định / Ollama cục bộ) chuyển bằng `.env`; Qdrant
  làm vector DB; chỉ trả lời theo tri thức nội bộ, từ chối bịa khi ngoài phạm vi.
- Trang chat `/assistant` trong dx-portal + proxy an toàn tới DX-RAG.
- Tài liệu tri thức mẫu (SOP tiếp nhận ticket, chính sách bảo hành/đổi trả).
- Service `qdrant`, `dx-rag`, và `ollama` (profile `local-llm`) trong docker-compose.
- **DX-Diag — Chẩn đoán độ trưởng thành HPDI** (route `/diag` trong dx-portal):
  khảo sát 12 câu trên 4 trục H-P-D-I, thuật toán chấm điểm, biểu đồ radar (SVG thuần)
  và khuyến nghị trục cần ưu tiên theo nguyên lý tiến hóa tuyến tính. Kiểm chứng bằng
  Chrome headless. Đây là artifact khác biệt hóa đặc thù của cuộc thi.

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
