# DX-Lab OSS

> **Trạm Thực hành Hệ điều hành Doanh nghiệp số bằng Mã nguồn mở**
> Sản phẩm dự thi **Olympic Tin học Sinh viên Việt Nam 2026 — Nội dung Phần mềm Nguồn mở (PMNM)**.
> Chủ đề: *Xây dựng Hệ điều hành Doanh nghiệp số (DX-OS)* dựa trên kiến trúc Open-Core.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

DX-Lab OSS tái hiện đầy đủ **4 không gian kiến trúc H-P-D-I** của mô hình DX-OS bằng một
ngăn xếp **100% phần mềm nguồn mở (OSI-approved)**, triển khai chỉ với **một lệnh**, giúp
doanh nghiệp vừa và nhỏ (SME) vận hành số mà không phụ thuộc phần mềm bản quyền nguồn đóng.

---

## Vấn đề giải quyết

Phần lớn chương trình chuyển đổi số của SME rơi vào bẫy **"ảo tưởng công nghệ"**: mua nhiều
phần mềm nhưng nhân sự vẫn nhắn tin rải rác, báo cáo thủ công, dữ liệu bị giam trong các ốc
đảo thông tin. DX-Lab OSS đập tan bẫy này bằng một hệ điều hành số tích hợp, kỷ luật dữ liệu
từ đầu nguồn ("chống rác đầu vào — rác đầu ra").

Chi tiết pain point & giải pháp: xem [docs/du-an.md](docs/du-an.md).
Kiến trúc hệ thống & ảnh demo: xem [docs/kien-truc.md](docs/kien-truc.md).

## Kiến trúc H-P-D-I

| Không gian | Chức năng | Nền tảng nguồn mở | Thành phần tự viết |
|-----------|-----------|-------------------|--------------------|
| **[H] Human** | SSO, cổng thông tin, lưu trữ P.A.R.A | Keycloak · Nextcloud | **DX-Portal** (Next.js) |
| **[P] Process** | Biểu mẫu, Poka-yoke, phân công/SLA tự động | Baserow | **DX-Core** (trục sự kiện) |
| **[D] Data** | Nguồn sự thật duy nhất, dashboard, dữ liệu mở liên kết | PostgreSQL · Metabase | **Open-Data API** (JSON-LD/DCAT) |
| **[I] Intelligence** | RAG chống ảo giác | Qdrant · Gemini API / Ollama | **DX-RAG** |

Thành phần đặc thù: **DX-Diag** — công cụ chẩn đoán độ trưởng thành số HPDI (DTI).

> Lộ trình mở rộng (chưa triển khai): Rocket.Chat (giao tiếp nội bộ),
> Node-RED (automation trực quan). Xem [docs/du-an.md](docs/du-an.md).

## Bắt đầu nhanh (Quickstart)

> Yêu cầu: Docker & Docker Compose. Khuyến nghị ≥ 8GB RAM (hoặc dùng LLM qua API — xem `.env`).

```bash
# 1. Sao chép cấu hình
cp .env.example .env      # rồi sửa mật khẩu trong .env

# 2. Dựng toàn bộ hệ thống
docker compose up -d

# 3. Truy cập
#   DX-Portal   → http://localhost:3000
#   Keycloak    → http://localhost:8080
#   Baserow     → http://localhost:8085
#   Metabase    → http://localhost:3001
```

Hướng dẫn build từ mã nguồn đầy đủ: [docs/build-from-source.md](docs/build-from-source.md) *(đang cập nhật)*.

## Cấu trúc kho mã

```
src/dx-core/      Trục sự kiện + rule engine (FastAPI)
src/dx-portal/    Cổng SSO nguồn sự thật (Next.js)
src/dx-diag/      Chẩn đoán trưởng thành HPDI
src/dx-rag/       RAG + Agent nghiệp vụ (FastAPI)
src/platforms/    Cấu hình nền tảng bên thứ ba (không sửa mã upstream)
config/ schemas/ seed/ examples/   Cấu hình, lược đồ, dữ liệu mẫu
docs/             Tài liệu kiến trúc, đề bài, kịch bản
```

## Giấy phép

Mã nguồn của đội phát hành theo giấy phép [MIT](LICENSE). Giấy phép các thành phần bên thứ ba
được liệt kê tại [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Đóng góp & Cộng đồng

Xem [CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) ·
[SECURITY.md](SECURITY.md). Báo lỗi qua [GitHub Issues](../../issues).

---

*Sản phẩm dự thi OLP PMNM 2026 · Bảo trợ chuyên môn: Hội Tin học Việt Nam & CLB VFOSSA.*
