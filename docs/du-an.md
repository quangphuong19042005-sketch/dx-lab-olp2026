# DỰ ÁN DỰ THI OLP PMNM 2026 — DX-Lab OSS

> **Trạm Thực hành Hệ điều hành Doanh nghiệp số bằng Mã nguồn mở**
> Đề xuất giải pháp cho chủ đề *"Xây dựng Hệ điều hành Doanh nghiệp số (DX-OS)"* — Cuộc thi Phần mềm Nguồn mở, Olympic Tin học Sinh viên Việt Nam 2026.

- **Tài liệu nền:** [Thể lệ cuộc thi](the-le-cuoc-thi-pmnm-olp-2026.md) · [Quick Guide DX-OS](quick-guide-to-dxos.md) · [Giáo trình DX-OS đầy đủ](dx-os/README.md)
- **Kho mã nguồn:** `dx-lab-olp2026` (công khai trên GitHub/GitLab)
- **Trạng thái:** Bản đề xuất v1 — chờ chốt kịch bản nghiệp vụ demo và phân công đội.

---

## 0. Tóm tắt điều hành

**DX-Lab OSS** là một *hệ điều hành doanh nghiệp số* lắp ráp hoàn toàn từ phần mềm nguồn mở (OSI-approved), triển khai **một lệnh `docker compose up`**, tái hiện đủ 4 không gian kiến trúc **H-P-D-I** mà giáo trình DX-OS mô tả — nhưng thay thế toàn bộ ngăn xếp Google Workspace (nguồn đóng) bằng các nền tảng lõi mở tương đương.

Điểm nguyên gốc (originality) của đội không nằm ở việc "cài lại phần mềm người khác", mà ở **lõi tích hợp tự viết `DX-Core`** khâu nối các nền tảng rời rạc thành một cỗ máy vận hành thống nhất, cộng với **công cụ chẩn đoán độ trưởng thành HPDI** — một sản phẩm đặc thù của cuộc thi mà gần như không đội nào khác có.

> **Một câu giá trị:** *"Biến 900.000 SME Việt Nam từ nạn nhân của 'ảo tưởng công nghệ' thành chủ nhân của một hệ điều hành số 0 đồng bản quyền — chạy được trên một chiếc máy chủ duy nhất."*

---

## 1. Pain point thực tế — vấn đề chúng ta giải quyết

Giải pháp phải bám đúng **nỗi đau vận hành có thật** của SME, không phải một demo công nghệ trưng bày. Dưới đây là 6 pain point cốt lõi (trích chứng từ giáo trình DX-OS và thực tế thị trường):

| # | Pain point thực tế | Hệ quả | Nguồn |
|---|--------------------|--------|-------|
| P1 | **"Ảo tưởng công nghệ"** — mua nhiều phần mềm đắt tiền nhưng nhân sự vẫn làm theo thói quen cũ | Chi tiền tỷ mà không tăng năng lực; ROI âm | Lời mở đầu, Quick Guide §1 |
| P2 | **"Zalo hóa" / nhắn tin rải rác** — yêu cầu công việc trôi trong chat, không truy vết được | Việc rơi rớt, không ai chịu trách nhiệm, không có SLA | Giáo trình 5.5, 4.2.1 |
| P3 | **Ốc đảo thông tin (data silo)** — mỗi bộ phận một file Excel, không có "nguồn sự thật duy nhất" | Số liệu lệch nhau, báo cáo mâu thuẫn | Quick Guide §1.1 [D] |
| P4 | **Báo cáo thủ công, "khám nghiệm tử thi"** — lãnh đạo chờ Excel cuối tháng, ra quyết định bằng cảm tính | Phản ứng chậm, mất cơ hội | Lời mở đầu, 4.2.3 |
| P5 | **"Rác đầu vào — Rác đầu ra"** — dữ liệu bẩn từ đầu nguồn, không có rào chắn nhập liệu | AI/BI vô dụng, sinh ảo giác dữ liệu | 1.3, Quick Guide §1.2 |
| P6 | **Phụ thuộc nền tảng nguồn đóng** — chi phí bản quyền tăng theo quy mô, mất chủ quyền dữ liệu | Bị khóa nhà cung cấp (vendor lock-in), rủi ro pháp lý dữ liệu | 7.3 Chủ quyền số |

> **Nguyên tắc thiết kế:** mỗi tính năng trong sản phẩm phải truy vết ngược được về ít nhất một pain point ở trên (xem bảng truy vết §8). Không xây tính năng "cho đẹp".

---

## 2. Ràng buộc & luật chơi cuộc thi (bám sát để không mất điểm)

Thang điểm **100 = 50 PoF + 50 Sản phẩm**. PoF (Point of Failure) chấm *trước* chung kết, thuần về kỷ luật nguồn mở — **đây là 50 điểm dễ mất nhất và dễ giành nhất**.

**Nhóm PoF (50đ) — bắt buộc:**
- Kho mã nguồn công khai trên Internet, có web viewer, thực sự được sử dụng (commit đều).
- Giấy phép **OSI-approved**, ghi rõ trong **từng tệp mã**, kèm **bản sao toàn văn** giấy phép, không xung đột giấy phép.
- Có ít nhất **1 bản release** trước hạn nộp, phát hành theo phiên bản, định dạng mở.
- **Build from source được** — có hướng dẫn dịch/cài, cấu hình không phải sửa tay header, không dùng công cụ nguồn đóng để dịch. **Khuyến khích Docker.**
- Thư viện đính kèm: **không sửa mã nguồn thư viện bên thứ ba**, làm rõ dependency, ưu tiên dùng bản upstream.
- Tài liệu: có **README**, **CHANGELOG**, **bug tracker** (GitHub Issues).

**Nhóm Sản phẩm (50đ) — chấm tại chung kết:**
- Tính nguyên gốc của giải pháp kỹ thuật (10) · Mức độ hoàn thiện (10) · Thân thiện người dùng (10) · Phát triển bền vững (10) · Phong cách trình diễn & thu hút cộng đồng (10).

**Mốc thời gian:** Chủ đề công bố 7/2026 → **Đề thi chi tiết công bố 11/2026** → Chấm kho mã 7–9/12/2026 → Trình diễn chung kết 10/12/2026 → Trao giải 11/12/2026.

> ⚠️ **Lưu ý chiến lược:** đề thi *chi tiết* chỉ có vào 11/2026. Vì vậy dự án này thiết kế theo hướng **nền tảng lõi vững + mô-đun hóa**, để khi có đề cụ thể chỉ cần cấu hình lại kịch bản nghiệp vụ mà không phải viết lại kiến trúc.

---

## 3. Giải pháp: DX-Lab OSS

### 3.1. Tuyên ngôn kiến trúc

Giáo trình DX-OS dạy tư duy trên ngăn xếp **Google Workspace (nguồn đóng)**. Cuộc thi yêu cầu **Open-Core**. Đóng góp cốt lõi của đội là **phép ánh xạ (mapping) từng thành phần GWS sang một nền tảng nguồn mở tương đương**, rồi **tự viết lõi khâu nối** để chúng vận hành như một hệ điều hành thống nhất.

```
        ┌───────────────────────── DX-Portal (tự viết) ─────────────────────────┐
        │      Nguồn sự thật duy nhất · SSO · điều hướng nghiệp vụ · SOP        │
        └───────────────┬───────────────────────────────────┬──────────────────┘
                        │                                   │
   [H] HUMAN            │        [P] PROCESS                │   [D] DATA        [I] INTELLIGENCE
 ┌───────────────┐  ┌───┴──────────────┐          ┌─────────┴────────┐   ┌──────────────────┐
 │ Keycloak (SSO)│  │ Baserow/NocoDB   │          │ PostgreSQL (SSOT)│   │ Ollama + Qdrant  │
 │ Nextcloud     │  │ (low-code form + │          │ Metabase/Superset│   │ + DX-RAG (tự viết│
 │ (P.A.R.A)     │  │  DB + Poka-yoke) │          │ (BI dashboard)   │   │  agent nghiệp vụ)│
 │ Rocket.Chat   │  │ Node-RED/Windmill│          └──────────────────┘   └──────────────────┘
 │ + Telegram bot│  │ (automation/iPaaS)│
 └───────────────┘  └───┬──────────────┘
                        │
              ┌─────────┴──────────┐
              │  DX-Core (tự viết) │  ← Trục trung gian hướng sự kiện: chuẩn hóa event,
              │  Event Bus + Rules │    định tuyến, thực thi quy tắc nghiệp vụ, cấp phát tài khoản
              └────────────────────┘
```

### 3.2. Ánh xạ H-P-D-I: Google Workspace → Mã nguồn mở

| Không gian | Vai trò (theo giáo trình) | GWS (giáo trình) | **Thay bằng nguồn mở** | Giấy phép (cần xác minh khi build) |
|-----------|---------------------------|------------------|------------------------|-----------------------------------|
| **[H]** | Định danh tập trung / SSO | Google Admin | **Keycloak** | Apache-2.0 ✅ |
| **[H]** | Lưu trữ P.A.R.A | Google Drive | **Nextcloud** | AGPL-3.0 ✅ |
| **[H]** | Cổng thông tin nội bộ | Google Sites | **DX-Portal (tự viết)** | MIT (của đội) ✅ |
| **[H]** | Wiki/tri thức (SOP) | Google Docs | **BookStack** | MIT ✅ |
| **[H]** | Giao tiếp tức thời + cảnh báo | Telegram | **Rocket.Chat** + **Telegram Bot API** | MIT ✅ (bot chỉ là kênh, không ship) |
| **[P]** | CSDL phẳng + biểu mẫu | Google Sheets + Forms | **Baserow** (hoặc NocoDB) | MIT ✅ (Baserow core) / AGPL-3.0 (NocoDB) |
| **[P]** | Ứng dụng thao tác + Poka-yoke | AppSheet | **Baserow views** / **Budibase** | MIT ✅ / GPL-3.0 |
| **[P]** | Tự động hóa luồng (iPaaS) | n8n / Apps Script | **Node-RED** (hoặc Windmill) | Apache-2.0 ✅ / AGPL-3.0 |
| **[D]** | Nguồn sự thật duy nhất | Google Sheets | **PostgreSQL** | PostgreSQL License ✅ |
| **[D]** | Dashboard thời gian thực | Looker Studio | **Metabase** (hoặc Superset) | AGPL-3.0 ✅ / Apache-2.0 |
| **[I]** | LLM chống ảo giác (RAG) | NotebookLM | **Ollama + Qdrant + DX-RAG (tự viết)** | MIT / Apache-2.0 / MIT ✅ |
| **[I]** | Trợ lý tùy chỉnh (Agent) | Gemini Gems | **DX-Agent (tự viết, LlamaIndex)** | MIT ✅ |

> ⚠️ **Bẫy giấy phép — cực kỳ quan trọng cho 10đ PoF cấp phép:**
> - **n8n KHÔNG phải OSI-approved** (dùng "Sustainable Use License" / fair-code). **Dùng Node-RED (Apache-2.0) hoặc Windmill (AGPL-3.0) thay thế.**
> - **Open WebUI** có điều khoản hạn chế thương hiệu → **tự viết UI chat** cho không gian [I] thay vì đóng gói kèm.
> - Trộn AGPL (Nextcloud, Metabase, NocoDB) với MIT (code của đội) **hợp lệ** vì các thành phần chạy như **tiến trình độc lập giao tiếp qua API/mạng** (không link tĩnh) → không lây nhiễm giấy phép. Vẫn phải ghi rõ trong `NOTICE`/`THIRD_PARTY_LICENSES`.
> - **Không sửa mã nguồn** bất kỳ thư viện/nền tảng bên thứ ba nào — chỉ dùng image upstream + file cấu hình bên ngoài (thỏa tiêu chí "không chỉnh sửa gói đính kèm").

### 3.3. Bốn thành phần NGUYÊN GỐC tự viết (nơi ghi điểm sáng tạo)

Đây là phần code mang giấy phép của đội, là "linh hồn" biến một mớ container thành một sản phẩm:

1. **`DX-Core` — Trục trung gian hướng sự kiện (Event Bus + Rule Engine).**
   Nhận webhook từ Baserow/Nextcloud, chuẩn hóa thành event thống nhất, định tuyến tới Node-RED/Rocket.Chat/Telegram, và thực thi quy tắc nghiệp vụ (SLA, phân công, leo thang). Đây chính là *"trục trung gian hướng sự kiện"* mà giáo trình chương 6.3 đòi hỏi. **(FastAPI/Node — MIT)**

2. **`DX-Portal` — Nguồn sự thật duy nhất.**
   Trang cổng nội bộ đăng nhập SSO (OIDC qua Keycloak), gom bảng tin, SOP, nút phóng nghiệp vụ, nhúng dashboard. Giải quyết pain "không biết link phần mềm ở đâu". **(Next.js/React — MIT)**

3. **`DX-Diag` — Công cụ chẩn đoán độ trưởng thành HPDI (DTI).**
   Bộ khảo sát "bắt mạch" tổ chức → thuật toán ánh xạ điểm → biểu đồ radar 4 trục H-P-D-I + khuyến nghị lỗ hổng cần đầu tư. **Đây là sản phẩm đặc thù của cuộc thi, gần như không đội nào khác có → khác biệt hóa mạnh.** Bám sát giáo trình 2.2–2.4. **(MIT)**

4. **`DX-RAG` / `DX-Agent` — Trợ lý nghiệp vụ tự hành chống ảo giác.**
   RAG bám kho P.A.R.A trên Nextcloud (chỉ trả lời theo SOP nội bộ), cộng tác tử tự động phân loại & định tuyến yêu cầu. Giải quyết pain "AI bịa chuyện" và "rác đầu vào". **(Python + LlamaIndex + Qdrant + Ollama — MIT)**

Cộng thêm **`deploy/` — một lệnh dựng cả hệ thống** (`docker compose up` + `Makefile` + seed data) → ghi thẳng điểm PoF "Building From Source" và điểm khuyến khích container hóa.

---

## 4. Kịch bản nghiệp vụ demo (vertical)

Để pain point "sờ thấy được" khi trình diễn, ta neo vào một kịch bản SME cụ thể. **Đề xuất chính (mặc định):** *"Hệ thống Tiếp nhận Yêu cầu & Xử lý Sự vụ khách hàng — DX-Ticket"* cho một SME dịch vụ/thương mại. Đây là ví dụ kinh điển của chính giáo trình (Hộp cát DX-Lab dùng DX-Ticket), ban giám khảo quen thuộc, và ánh xạ trọn vẹn cả 4 không gian.

**Hành trình xuyên 4 tác nhân (dùng để dựng kịch bản showcase):**

1. **Khách hàng** gửi yêu cầu qua **biểu mẫu Baserow** (có rào chắn định dạng SĐT/email — Poka-yoke) → chặn rác đầu vào (P5).
2. **`DX-Core`** bắt event → tạo ticket trong PostgreSQL → tự phân công theo quy tắc → bắn cảnh báo vào **Telegram/Rocket.Chat** đúng luồng chủ đề (P2).
3. **Nhân viên** đăng nhập **DX-Portal (SSO)**, xử lý ticket trên ứng dụng Baserow di động, buộc đính kèm bằng chứng mới được đóng (Poka-yoke) (P1, P5).
4. **`DX-Agent`** gợi ý câu trả lời dựa trên SOP trong Nextcloud (không bịa) (P5).
5. **Lãnh đạo** mở **Metabase dashboard** thấy SLA, tồn đọng, hiệu suất theo thời gian thực thay vì chờ Excel cuối tháng (P3, P4).
6. Bất cứ lúc nào, chạy **DX-Diag** để chấm điểm trưởng thành số của tổ chức và đề xuất bước tiến hóa tiếp theo.

**Các vertical thay thế (có thể hoán đổi khi có đề chi tiết 11/2026 hoặc theo thế mạnh đội):**
- **Đơn hàng đa kênh (order-to-cash)** cho hộ kinh doanh/bán lẻ — pain "đơn trôi trên Zalo/Facebook, không đồng bộ tồn kho" rất đời thường.
- **Dịch vụ kỹ thuật hiện trường** (điện lạnh, bảo trì) — Poka-yoke "bắt buộc chụp ảnh GPS" trình diễn cực trực quan.
- **Tuyển sinh & quản lý học viên** cho trung tâm đào tạo/nhà trường.

> Nhờ thiết kế mô-đun, đổi vertical = đổi cấu hình bảng dữ liệu + luồng automation + prompt, **không** đổi kiến trúc.

---

## 5. Kiến trúc kỹ thuật & triển khai

- **Đóng gói:** mỗi nền tảng một container; toàn hệ thống dựng bằng **một** `docker-compose.yml` + `.env.example`. Có `Makefile` (`make up`, `make seed`, `make demo`).
- **SSO xuyên suốt:** Keycloak là OIDC provider; Nextcloud, Rocket.Chat, Baserow, Metabase, DX-Portal đều liên kết → đúng tinh thần "hộ chiếu số" & "cắt quyền 1 chạm".
- **Luồng dữ liệu:** Baserow (nhập) → PostgreSQL (SSOT) → Metabase (đọc, không đổi gốc) → Qdrant/DX-RAG (tri thức). DX-Core là trục sự kiện nối tất cả.
- **Chạy được trên 1 VPS** (khuyến nghị ≥ 8GB RAM do có LLM cục bộ; hỗ trợ cấu hình gọi LLM ngoài nếu máy yếu).
- **Cấu hình bằng biến môi trường** (không sửa header) → thỏa PoF.

---

## 6. Cấu trúc kho mã nguồn đề xuất

Cấu trúc dưới đây được **mô phỏng theo repo đội OLP 2025 [UrbanReflex](https://github.com/minhe51805/UrbanReflex)** (HUTECH + VFOSSA) — một layout đã được kiểm chứng là tối ưu cho điểm PoF, có bổ sung các thư mục đặc thù DX-Lab:

```
dx-lab-olp2026/
├── README.md                  # Giới thiệu, kiến trúc, quickstart (bắt buộc PoF)
├── LICENSE                     # Bản toàn văn giấy phép OSI
├── CHANGELOG.md                # Lịch sử phiên bản (bắt buộc PoF)
├── CONTRIBUTING.md             # Hướng dẫn đóng góp — thu hút cộng đồng nguồn mở
├── CODE_OF_CONDUCT.md          # Quy tắc ứng xử (chuẩn dự án OSS bền vững)
├── SECURITY.md                 # Chính sách bảo mật / báo lỗi
├── THIRD_PARTY_LICENSES.md     # Giấy phép mọi thành phần bên thứ ba
├── .github/
│   └── ISSUE_TEMPLATE/         # Bug tracker chuyên nghiệp (bắt buộc PoF)
├── .env.example                # Cấu hình bằng biến môi trường (không sửa header)
├── .gitignore  .dockerignore
├── .pre-commit-config.yaml     # Tự động kiểm tra chất lượng mã trước commit
├── .justfile / Makefile        # Task runner một lệnh (just install / make up)
├── pyproject.toml  biome.json  .prettierrc.json   # Chuẩn lint/format
├── docker-compose.yml          # Dựng TOÀN hệ thống 1 lệnh (điểm container hóa)
├── config/                     # Cấu hình tập trung
├── schemas/                    # Lược đồ dữ liệu (SSOT, linked data)
├── seed/                       # Dữ liệu mẫu cho kịch bản demo
├── examples/                   # Ví dụ API / payload
├── docs/                       # Kiến trúc, hướng dẫn build, kịch bản showcase
└── src/
    ├── dx-core/                # Trục sự kiện + rule engine (tự viết)
    ├── dx-portal/              # Cổng SSO nguồn sự thật (tự viết, Next.js)
    ├── dx-diag/                # Chẩn đoán trưởng thành HPDI (tự viết)
    ├── dx-rag/                 # RAG + Agent nghiệp vụ (tự viết, FastAPI)
    └── platforms/              # File cấu hình Keycloak/Baserow/Metabase (KHÔNG sửa mã upstream)
```

Mỗi tệp mã tự viết **phải có header giấy phép** (SPDX, ví dụ `// SPDX-License-Identifier: MIT`) — nên tạo commit riêng "add license headers" như đội 2025 để ghi dấu rõ ràng cho giám khảo.

### 6.1. Bài học rút ra từ đội OLP 2025 (UrbanReflex)

Repo UrbanReflex (chủ đề Dữ liệu mở 2025) là tham chiếu thực chiến quý giá — cùng bảo trợ HUTECH + VFOSSA:

| Yếu tố họ làm tốt | Ta áp dụng |
|-------------------|-----------|
| Đủ bộ file OSS gốc (README, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE) | Bê nguyên bộ này từ G0 |
| `.github/ISSUE_TEMPLATE` làm bug tracker | Bắt buộc |
| Pre-commit + Husky + lint (Black/Flake8/ESLint/Prettier/Biome) | Bắt buộc — giám khảo nhìn commit history thấy kỷ luật |
| Task runner `just` + `docker compose` → cài **một lệnh** | `just install` / `docker compose up` |
| Monorepo `src/backend` (FastAPI) + `src/frontend` (Next.js 16) | DX-RAG/DX-Core = FastAPI; DX-Portal/DX-Diag = Next.js |
| Commit riêng "add license headers to source files" | Làm y hệt |
| GPL-3.0, header trong từng tệp | Ta chọn MIT/Apache-2.0 (linh hoạt hơn), vẫn header từng tệp |
| Dùng **Gemini + Pinecone (SaaS)** qua API mà vẫn hợp lệ | ✅ **Tiền lệ quan trọng:** gọi AI qua API lúc chạy KHÔNG vi phạm PoF (không phải thư viện đính kèm) → ta có thể hỗ trợ **cả** Ollama cục bộ **và** API ngoài (cấu hình bằng `.env`), gỡ nút thắt "máy demo yếu" |
| 624 commit, PR review, nhiều branch/tag | Commit đều tay, làm việc qua PR, release theo tag |

> **Khác biệt hóa của ta so với 2025:** UrbanReflex tập trung *một* trục (dữ liệu mở đô thị). DX-Lab OSS phải thể hiện **đủ 4 không gian H-P-D-I tích hợp thành hệ điều hành** — tham vọng hơn, nên càng phải kỷ luật mô-đun và ưu tiên luồng lõi chạy trọn vẹn.

---

## 7. Lộ trình triển khai (bám mốc cuộc thi)

| Giai đoạn | Thời gian | Mục tiêu | Đầu ra |
|-----------|-----------|----------|--------|
| **G0 — Nền móng** | 7–8/2026 | Dựng repo, license, CI, docker-compose khung; SSO Keycloak chạy | Repo công khai + release `v0.1` |
| **G1 — Không gian [H]+[P]** | 9/2026 | Nextcloud P.A.R.A, Baserow form + Poka-yoke, DX-Core event bus, Rocket.Chat/Telegram alert | Luồng ticket end-to-end chạy được |
| **G2 — Không gian [D]+[I]** | 10/2026 | Metabase dashboard, DX-RAG/Agent bám SOP, DX-Diag | Demo 4 không gian hoàn chỉnh |
| **G3 — Hoàn thiện & tài liệu** | 11/2026 | README/CHANGELOG/bugtracker, dọn giấy phép từng tệp, tối ưu UX | Release `v1.0` + tài liệu PoF đầy đủ |
| **G4 — Bám đề chi tiết** | sau 11/2026 | Cấu hình kịch bản theo đề BTC công bố; luyện showcase | Bản trình diễn chung kết |
| **G5 — Chung kết** | 7–11/12/2026 | Nộp kho mã, trình diễn, thu hút cộng đồng | — |

> **Kỷ luật PoF ngay từ G0:** license header, CHANGELOG, Issues, release theo phiên bản **làm từ đầu** — không để cuối mới dọn (dễ mất 50đ oan).

---

## 8. Bảng truy vết: Pain point → Giải pháp

| Pain | Thành phần giải quyết |
|------|----------------------|
| P1 Ảo tưởng công nghệ | DX-Diag (đo trước–sau) + hệ 0 đồng bản quyền chứng minh giá trị không phụ thuộc chi tiền |
| P2 Zalo hóa, việc trôi | DX-Core route event → Rocket.Chat/Telegram theo chủ đề, ticket có SLA & truy vết |
| P3 Ốc đảo thông tin | PostgreSQL làm SSOT + Baserow là điểm nhập duy nhất |
| P4 Báo cáo tử thi | Metabase dashboard thời gian thực |
| P5 Rác đầu vào | Poka-yoke ở Baserow + DX-RAG chống ảo giác (chỉ trả lời theo SOP) |
| P6 Nguồn đóng, khóa nhà cung cấp | Toàn bộ ngăn xếp OSI, self-host, chủ quyền dữ liệu |

---

## 9. Chiến lược ghi điểm

**PoF (50đ) — checklist bắt buộc trước 12/2026:**
- [ ] Kho công khai + web viewer + commit đều tay
- [ ] LICENSE toàn văn + SPDX header **từng tệp** + THIRD_PARTY_LICENSES + không xung đột
- [ ] ≥ 1 release theo phiên bản, định dạng mở (tag git)
- [ ] `docker compose up` dựng được từ mã nguồn; hướng dẫn build rõ; không sửa header thủ công
- [ ] Không sửa mã thư viện bên thứ ba; khai báo dependency đầy đủ
- [ ] README + CHANGELOG + GitHub Issues (bug tracker)

**Sản phẩm (50đ) — vũ khí tại chung kết:**
- **Nguyên gốc (10):** DX-Core + DX-Diag là điểm nhấn ít đội có.
- **Hoàn thiện (10):** demo end-to-end mượt, không lỗi.
- **Thân thiện (10):** một cổng DX-Portal, một lần đăng nhập, giao diện tiếng Việt.
- **Bền vững (10):** tài liệu kiến trúc, CONTRIBUTING, lộ trình roadmap công khai.
- **Trình diễn (10):** kịch bản kể chuyện theo hành trình 6 bước §4, nhấn "0 đồng bản quyền" và "chủ quyền dữ liệu".

---

## 10. Rủi ro & giảm thiểu

| Rủi ro | Mức | Giảm thiểu |
|--------|-----|-----------|
| Dùng nhầm phần mềm **không OSI** (n8n, Outline, Open WebUI) → mất điểm cấp phép | Cao | Chốt danh mục OSI §3.2 ngay từ G0; rà `THIRD_PARTY_LICENSES` mỗi release |
| LLM cục bộ nặng máy demo | TB | Ollama model nhỏ + cờ cấu hình gọi API ngoài dự phòng |
| Ôm đồm quá nhiều nền tảng, không kịp hoàn thiện | Cao | Ưu tiên luồng lõi DX-Ticket end-to-end; thành phần phụ để "nice-to-have" |
| Đề chi tiết 11/2026 lệch kịch bản | TB | Kiến trúc mô-đun; vertical hoán đổi bằng cấu hình (§4) |
| Xung đột file khi 3 người code chung | TB | Phân quyền sở hữu theo `services/*` (§11), commit nhỏ, PR review |

---

## 11. Phân công đội (3 thành viên + 1 giảng viên dẫn dắt)

| Vai trò | Sở hữu | Trọng tâm |
|---------|--------|-----------|
| **Dev 1 — Platform/DevOps** | `docker-compose`, `platforms/`, Keycloak/Nextcloud/Rocket.Chat | Hạ tầng, SSO, đóng gói, PoF build-from-source |
| **Dev 2 — Backend/Integration** | `services/dx-core`, `services/dx-rag`, PostgreSQL, Node-RED | Trục sự kiện, automation, AI agent |
| **Dev 3 — Frontend/Data** | `services/dx-portal`, `services/dx-diag`, Baserow, Metabase | Cổng thông tin, chẩn đoán HPDI, dashboard, UX |
| **Giảng viên** | Định hướng nghiệp vụ, review kiến trúc, luyện showcase | — |

---

## 12. Bước tiếp theo (đề xuất chốt ngay)

1. **Chốt vertical demo** (mặc định: DX-Ticket) và **danh mục công cụ OSI** (Baserow vs NocoDB, Node-RED vs Windmill, Metabase vs Superset).
2. `git init` + tạo kho công khai + chọn giấy phép (đề xuất **MIT** cho code đội — đơn giản, tương thích rộng).
3. Dựng khung `docker-compose` + Keycloak SSO như release `v0.1`.
4. Sau khi chốt, tôi có thể tách tài liệu này thành **kế hoạch `plans/` chi tiết theo từng phase** để bắt tay code.

> *Tài liệu này là bản đề xuất định hướng. Mọi thông tin giấy phép cần được xác minh lại theo đúng phiên bản phần mềm tại thời điểm build (nguyên tắc "không đoán bừa" về pháp lý nguồn mở).*
