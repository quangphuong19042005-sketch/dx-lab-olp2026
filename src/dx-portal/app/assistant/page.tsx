// SPDX-License-Identifier: MIT
"use client";
import Link from "next/link";
import { useState } from "react";

interface Msg { role: "user" | "bot"; text: string; sources?: string[] }

const SAMPLES = [
  "SLA cho ticket ưu tiên cao là bao lâu?",
  "Ticket kỹ thuật được giao cho bộ phận nào?",
  "Chính sách bảo hành và đổi trả thế nào?",
];

export default function Assistant() {
  const [msgs, setMsgs] = useState<Msg[]>([]);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [reindexing, setReindexing] = useState(false);
  const [reindexMsg, setReindexMsg] = useState<string | null>(null);

  async function reindex() {
    setReindexing(true);
    setReindexMsg(null);
    try {
      const res = await fetch("/api/reindex", { method: "POST" });
      const d = await res.json();
      setReindexMsg(
        d.error
          ? d.error
          : `✅ Đã nạp ${d.ingested ?? 0} đoạn từ ${d.files ?? 0} tài liệu (nguồn: ${d.source ?? "?"}).`
      );
    } catch {
      setReindexMsg("Không kết nối được trợ lý.");
    } finally {
      setReindexing(false);
    }
  }

  async function ask(question: string) {
    if (!question.trim() || loading) return;
    setMsgs((m) => [...m, { role: "user", text: question }]);
    setQ("");
    setLoading(true);
    try {
      const res = await fetch("/api/assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setMsgs((m) => [...m, {
        role: "bot",
        text: data.answer || data.message || "Có lỗi xảy ra.",
        sources: data.sources,
      }]);
    } catch {
      setMsgs((m) => [...m, { role: "bot", text: "Không kết nối được trợ lý." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="main">
      <div className="container" style={{ paddingTop: 30 }}>
        <Link className="link-back" href="/">← Về trang chủ</Link>
        <div className="panel" style={{ maxWidth: 720 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
            <div>
              <h2>Trợ lý AI nội bộ</h2>
              <p className="sub">
                Hỏi đáp dựa trên tài liệu &amp; quy trình nội bộ. Trợ lý chỉ trả lời theo tri thức
                đã nạp (chống bịa đặt).
              </p>
            </div>
            <button
              onClick={reindex}
              disabled={reindexing}
              title="Nạp lại tri thức từ kho tài liệu P.A.R.A (Nextcloud)"
              style={{
                whiteSpace: "nowrap", background: "#f1f5f9", border: "1px solid var(--line)",
                borderRadius: 10, padding: "8px 14px", fontSize: 13, cursor: "pointer", color: "var(--ink)",
              }}
            >
              {reindexing ? "Đang nạp…" : "🔄 Nạp lại tri thức"}
            </button>
          </div>
          {reindexMsg && <div className="alert ok" style={{ marginBottom: 14 }}>{reindexMsg}</div>}

          {msgs.length === 0 && (
            <div style={{ marginBottom: 16 }}>
              <div className="hint" style={{ marginBottom: 8 }}>Gợi ý câu hỏi:</div>
              {SAMPLES.map((s) => (
                <button key={s} className="chip" onClick={() => ask(s)}>{s}</button>
              ))}
            </div>
          )}

          <div className="chat">
            {msgs.map((m, i) => (
              <div key={i} className={`bubble ${m.role}`}>
                {m.text}
                {m.sources && m.sources.length > 0 && (
                  <div className="src">📎 Nguồn: {m.sources.join(", ")}</div>
                )}
              </div>
            ))}
            {loading && <div className="bubble bot">Đang tra cứu…</div>}
          </div>

          <form onSubmit={(e) => { e.preventDefault(); ask(q); }} style={{ display: "flex", gap: 8, marginTop: 14 }}>
            <input value={q} onChange={(e) => setQ(e.target.value)}
              placeholder="Nhập câu hỏi..." style={{ flex: 1 }} />
            <button className="btn" type="submit" disabled={loading}>Hỏi</button>
          </form>
        </div>
      </div>
    </main>
  );
}
