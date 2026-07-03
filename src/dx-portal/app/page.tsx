// SPDX-License-Identifier: MIT
import Link from "next/link";
import { links } from "./links";

export default function Home() {
  return (
    <>
      <header className="header">
        <div className="container">
          <div className="brand">
            <div className="logo">DX</div>
            <div>
              <h1>DX-Portal</h1>
              <small>Nguồn sự thật duy nhất · DX-Lab OSS</small>
            </div>
          </div>
          <div className="hero">
            <h2>Trung tâm điều hành doanh nghiệp số</h2>
            <p>
              Một cửa ngõ duy nhất cho mọi nghiệp vụ, dữ liệu và công cụ — vận hành
              trên nền tảng 100% mã nguồn mở theo kiến trúc H-P-D-I.
            </p>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <div className="section-title">Nghiệp vụ</div>
          <div className="grid">
            <Link className="card" href="/ticket">
              <span className="tag">Biểu mẫu</span>
              <div className="space-badges"><span className="badge p">[P] Process</span></div>
              <h3>Gửi yêu cầu / Ticket →</h3>
              <p>Tiếp nhận yêu cầu khách hàng với rào chắn chống nhập sai (Poka-yoke).</p>
            </Link>

            <a className="card" href={links.metabase} target="_blank" rel="noreferrer">
              <span className="tag">Dashboard</span>
              <div className="space-badges"><span className="badge d">[D] Data</span></div>
              <h3>Bảng điều khiển vận hành →</h3>
              <p>Giám sát SLA, tồn đọng, hiệu suất theo thời gian thực (Metabase).</p>
            </a>

            <Link className="card" href="/diag">
              <span className="tag">Chẩn đoán</span>
              <div className="space-badges">
                <span className="badge h">H</span><span className="badge p">P</span>
                <span className="badge d">D</span><span className="badge i">I</span>
              </div>
              <h3>Chẩn đoán trưởng thành số →</h3>
              <p>Tự "bắt mạch" tổ chức theo mô hình HPDI, nhận biểu đồ radar &amp; khuyến nghị.</p>
            </Link>

            <Link className="card" href="/assistant">
              <span className="tag">Trợ lý AI</span>
              <div className="space-badges"><span className="badge i">[I] Intelligence</span></div>
              <h3>Trợ lý AI nội bộ →</h3>
              <p>Hỏi đáp quy trình, chính sách — trả lời bám tài liệu nội bộ, không bịa.</p>
            </Link>
          </div>

          <div className="section-title">Công cụ hệ thống</div>
          <div className="grid">
            <a className="card" href={links.keycloak} target="_blank" rel="noreferrer">
              <div className="space-badges"><span className="badge h">[H] Human</span></div>
              <h3>Định danh & SSO →</h3>
              <p>Quản trị tài khoản tập trung, đăng nhập một lần (Keycloak).</p>
            </a>
            <a className="card" href={links.dxCoreDocs} target="_blank" rel="noreferrer">
              <div className="space-badges"><span className="badge p">[P] Process</span></div>
              <h3>DX-Core API →</h3>
              <p>Trục trung gian hướng sự kiện: chuẩn hóa, phân công, cảnh báo.</p>
            </a>
            <a className="card" href={links.baserow} target="_blank" rel="noreferrer">
              <div className="space-badges"><span className="badge p">[P] Process</span></div>
              <h3>Baserow (Low-code) →</h3>
              <p>Cơ sở dữ liệu phẳng &amp; biểu mẫu low-code (bật khi cần).</p>
            </a>
          </div>
        </div>
      </main>

      <footer className="footer">
        DX-Lab OSS · Sản phẩm dự thi OLP PMNM 2026 · Giấy phép MIT
      </footer>
    </>
  );
}
