# Giấy phép các thành phần bên thứ ba

DX-Lab OSS **lắp ráp** các nền tảng nguồn mở dưới đây dưới dạng **container/dịch vụ độc lập**,
giao tiếp qua API/mạng. Mã nguồn của đội (giấy phép MIT) **không** liên kết tĩnh (static link)
với các thành phần này, do đó không phát sinh lây nhiễm giấy phép (kể cả với AGPL).

Chúng tôi **không chỉnh sửa mã nguồn** của bất kỳ thành phần nào — chỉ dùng bản phát hành
chính thức (upstream) kèm file cấu hình bên ngoài.

## Đã triển khai (có trong `docker-compose.yml`)

| Thành phần | Phiên bản | Vai trò trong DX-Lab | Giấy phép | OSI |
|-----------|-----------|----------------------|-----------|-----|
| Keycloak | 26.0 | [H] Định danh / SSO (OIDC) | Apache-2.0 | ✅ |
| Nextcloud | 30 | [H] Lưu trữ tài liệu P.A.R.A (nguồn tri thức cho DX-RAG) | AGPL-3.0 | ✅ |
| PostgreSQL | 16 | [D] Nguồn sự thật duy nhất | PostgreSQL License | ✅ |
| Metabase | v0.51.8 | [D] BI Dashboard | AGPL-3.0 | ✅ |
| Qdrant | v1.12.4 | [I] Cơ sở dữ liệu véc-tơ | Apache-2.0 | ✅ |
| Baserow | 1.30.1 | [P] Low-code DB / Form | MIT (core) | ✅ |
| Ollama (tùy chọn, profile `local-llm`) | 0.5.4 | [I] Chạy LLM cục bộ | MIT | ✅ |

Thư viện đóng gói trong dịch vụ tự viết (khai báo tại `package.json` / `pyproject.toml`):
Next.js, next-auth, React (MIT) · FastAPI, httpx, psycopg, pydantic (MIT/BSD/Apache) — đều OSI-approved.

## Lộ trình mở rộng (CHƯA triển khai — định hướng kiến trúc)

Các thành phần dưới đây nằm trong bản thiết kế (xem [docs/du-an.md](docs/du-an.md)) nhưng **chưa
được tích hợp** vào bản hiện tại: **Rocket.Chat** (MIT, giao tiếp), **BookStack** (MIT, wiki/SOP),
**Node-RED** (Apache-2.0, automation trực quan). Tất cả đều OSI-approved, sẽ bổ sung ở các phiên bản sau.

## Lưu ý về lựa chọn giấy phép

- **Tránh dùng** các phần mềm **không** OSI-approved dù phổ biến: **n8n** (Sustainable Use
  License / fair-code), **Outline** (BSL), một số bản **Open WebUI** (hạn chế thương hiệu).
- Với dịch vụ AI gọi qua **API bên ngoài** lúc chạy (nếu cấu hình `LLM_MODE=api`): đây là
  *dịch vụ*, không phải thư viện đính kèm, nên không ảnh hưởng tính hợp lệ nguồn mở của sản phẩm.

> ⚠️ Mọi thông tin giấy phép cần được **xác minh lại theo đúng phiên bản** phần mềm tại thời
> điểm build. Bảng này sẽ được cập nhật khi khóa phiên bản (pin version) trong `docker-compose.yml`.
