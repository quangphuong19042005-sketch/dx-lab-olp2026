# Giấy phép các thành phần bên thứ ba

DX-Lab OSS **lắp ráp** các nền tảng nguồn mở dưới đây dưới dạng **container/dịch vụ độc lập**,
giao tiếp qua API/mạng. Mã nguồn của đội (giấy phép MIT) **không** liên kết tĩnh (static link)
với các thành phần này, do đó không phát sinh lây nhiễm giấy phép (kể cả với AGPL).

Chúng tôi **không chỉnh sửa mã nguồn** của bất kỳ thành phần nào — chỉ dùng bản phát hành
chính thức (upstream) kèm file cấu hình bên ngoài.

| Thành phần | Vai trò trong DX-Lab | Giấy phép | OSI |
|-----------|----------------------|-----------|-----|
| Keycloak | [H] Định danh / SSO (OIDC) | Apache-2.0 | ✅ |
| Nextcloud | [H] Lưu trữ P.A.R.A | AGPL-3.0 | ✅ |
| Rocket.Chat | [H] Giao tiếp nội bộ | MIT | ✅ |
| BookStack | [H] Wiki / SOP | MIT | ✅ |
| Baserow | [P] Low-code DB / Form | MIT (core) | ✅ |
| Node-RED | [P] Tự động hóa (iPaaS) | Apache-2.0 | ✅ |
| PostgreSQL | [D] Nguồn sự thật duy nhất | PostgreSQL License | ✅ |
| Metabase | [D] BI Dashboard | AGPL-3.0 | ✅ |
| Ollama | [I] Chạy LLM cục bộ | MIT | ✅ |
| Qdrant | [I] Cơ sở dữ liệu véc-tơ | Apache-2.0 | ✅ |
| LlamaIndex | [I] Khung RAG (thư viện) | MIT | ✅ |

## Lưu ý về lựa chọn giấy phép

- **Tránh dùng** các phần mềm **không** OSI-approved dù phổ biến: **n8n** (Sustainable Use
  License / fair-code), **Outline** (BSL), một số bản **Open WebUI** (hạn chế thương hiệu).
- Với dịch vụ AI gọi qua **API bên ngoài** lúc chạy (nếu cấu hình `LLM_MODE=api`): đây là
  *dịch vụ*, không phải thư viện đính kèm, nên không ảnh hưởng tính hợp lệ nguồn mở của sản phẩm.

> ⚠️ Mọi thông tin giấy phép cần được **xác minh lại theo đúng phiên bản** phần mềm tại thời
> điểm build. Bảng này sẽ được cập nhật khi khóa phiên bản (pin version) trong `docker-compose.yml`.
