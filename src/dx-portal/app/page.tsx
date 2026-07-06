// SPDX-License-Identifier: MIT
import Link from "next/link";
import { links } from "./links";
import { UserMenu } from "./UserMenu";

type Space = "h" | "p" | "d" | "i" | "hpdi";
interface CardItem {
  icon: string; space: Space; badge: React.ReactNode;
  title: string; desc: string; href: string; external?: boolean;
}

const badge = (s: Exclude<Space, "hpdi">, label: string) => (
  <span className={`badge ${s}`}>{label}</span>
);

const nghiepVu: CardItem[] = [
  { icon: "🎫", space: "p", badge: badge("p", "[P] Process"), href: "/ticket",
    title: "Gửi yêu cầu / Ticket", desc: "Tiếp nhận yêu cầu khách hàng với rào chắn chống nhập sai (Poka-yoke)." },
  { icon: "📊", space: "d", badge: badge("d", "[D] Data"), href: links.metabase, external: true,
    title: "Bảng điều khiển vận hành", desc: "Giám sát SLA, tồn đọng, hiệu suất theo thời gian thực (Metabase)." },
  { icon: "🧭", space: "hpdi", href: "/diag",
    badge: (<span className="space-badges"><span className="badge h">H</span><span className="badge p">P</span><span className="badge d">D</span><span className="badge i">I</span></span>),
    title: "Chẩn đoán trưởng thành số", desc: 'Tự "bắt mạch" tổ chức theo mô hình HPDI, nhận biểu đồ radar & khuyến nghị.' },
  { icon: "🤖", space: "i", badge: badge("i", "[I] Intelligence"), href: "/assistant",
    title: "Trợ lý AI nội bộ", desc: "Hỏi đáp quy trình, chính sách — trả lời bám tài liệu nội bộ, không bịa." },
];

const congCu: CardItem[] = [
  { icon: "🔐", space: "h", badge: badge("h", "[H] Human"), href: links.keycloak, external: true,
    title: "Định danh & SSO", desc: "Quản trị tài khoản tập trung, đăng nhập một lần (Keycloak)." },
  { icon: "📁", space: "h", badge: badge("h", "[H] Human"), href: links.nextcloud, external: true,
    title: "Kho tài liệu P.A.R.A", desc: "Lưu trữ SOP/tri thức chuẩn P.A.R.A (Nextcloud) — nguồn cho trợ lý AI." },
  { icon: "⚙️", space: "p", badge: badge("p", "[P] Process"), href: links.dxCoreDocs, external: true,
    title: "DX-Core API", desc: "Trục trung gian hướng sự kiện: chuẩn hóa, phân công, cảnh báo." },
  { icon: "🗃️", space: "p", badge: badge("p", "[P] Process"), href: links.baserow, external: true,
    title: "Baserow (Low-code)", desc: "Cơ sở dữ liệu phẳng & biểu mẫu low-code (bật khi cần)." },
  { icon: "🔗", space: "d", badge: badge("d", "[D] Data"), href: links.openData, external: true,
    title: "Cổng Dữ liệu mở", desc: "Xuất ticket dạng JSON-LD liên kết & CSV (DCAT, đã ẩn dữ liệu cá nhân)." },
];

function Card({ item }: { item: CardItem }) {
  const inner = (
    <>
      <div className="card-top">
        <div className="card-icon">{item.icon}</div>
        {item.badge}
      </div>
      <h3>{item.title} →</h3>
      <p>{item.desc}</p>
    </>
  );
  const cls = `card ${item.space}`;
  return item.external ? (
    <a className={cls} href={item.href} target="_blank" rel="noreferrer">{inner}</a>
  ) : (
    <Link className={cls} href={item.href}>{inner}</Link>
  );
}

export default function Home() {
  return (
    <>
      <header className="header">
        <div className="container">
          <div className="brand" style={{ justifyContent: "space-between" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div className="logo">DX</div>
              <div>
                <h1>DX-Portal</h1>
                <small>Nguồn sự thật duy nhất · DX-Lab OSS</small>
              </div>
            </div>
            <UserMenu />
          </div>
          <div className="hero">
            <h2>Trung tâm điều hành doanh nghiệp số</h2>
            <p>
              Một cửa ngõ duy nhất cho mọi nghiệp vụ, dữ liệu và công cụ — vận hành
              trên nền tảng 100% mã nguồn mở theo kiến trúc H-P-D-I.
            </p>
            <div className="hpdi-pills">
              <span className="hpdi-pill"><span className="dot" /> [H] Con người</span>
              <span className="hpdi-pill"><span className="dot" /> [P] Quy trình</span>
              <span className="hpdi-pill"><span className="dot" /> [D] Dữ liệu</span>
              <span className="hpdi-pill"><span className="dot" /> [I] Trí tuệ</span>
            </div>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <div className="section-title">Nghiệp vụ</div>
          <div className="grid">
            {nghiepVu.map((it) => <Card key={it.title} item={it} />)}
          </div>

          <div className="section-title">Công cụ hệ thống</div>
          <div className="grid">
            {congCu.map((it) => <Card key={it.title} item={it} />)}
          </div>
        </div>
      </main>

      <footer className="footer">
        DX-Lab OSS · Sản phẩm dự thi OLP PMNM 2026 · Giấy phép MIT
      </footer>
    </>
  );
}
