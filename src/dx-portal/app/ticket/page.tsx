// SPDX-License-Identifier: MIT
"use client";
import Link from "next/link";
import { useState } from "react";

type Result =
  | { ok: true; id: number; assignee: string; priority: string; sla: string }
  | { ok: false; message: string };

export default function TicketForm() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Result | null>(null);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    const fd = new FormData(e.currentTarget);
    const payload: Record<string, string> = {
      title: String(fd.get("title") || ""),
      description: String(fd.get("description") || ""),
      customer_name: String(fd.get("customer_name") || ""),
      customer_phone: String(fd.get("customer_phone") || ""),
      category: String(fd.get("category") || "khac"),
    };
    const pr = String(fd.get("priority") || "");
    if (pr) payload.priority = pr;

    try {
      const res = await fetch("/api/tickets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok) {
        setResult({
          ok: true, id: data.id, assignee: data.assignee,
          priority: data.priority, sla: data.sla_deadline,
        });
        e.currentTarget.reset();
      } else {
        setResult({ ok: false, message: data.message || "Dữ liệu không hợp lệ." });
      }
    } catch {
      setResult({ ok: false, message: "Không kết nối được máy chủ DX-Core." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="main">
      <div className="container" style={{ paddingTop: 30 }}>
        <Link className="link-back" href="/">← Về trang chủ</Link>
        <div className="panel">
          <h2>Gửi yêu cầu / Ticket</h2>
          <p className="sub">Yêu cầu sẽ được tự động phân loại, phân công và tính hạn xử lý (SLA).</p>

          {result?.ok && (
            <div className="alert ok">
              <strong>✅ Đã tiếp nhận ticket #{result.id}</strong>
              Giao cho <b>{result.assignee}</b> · Ưu tiên: {result.priority} · Hạn SLA:{" "}
              {new Date(result.sla).toLocaleString("vi-VN")}
            </div>
          )}
          {result && !result.ok && (
            <div className="alert err">
              <strong>⚠️ Chưa gửi được</strong>
              {result.message}
            </div>
          )}

          <form onSubmit={onSubmit}>
            <div className="field">
              <label>Tiêu đề yêu cầu *</label>
              <input name="title" required minLength={3} maxLength={200}
                placeholder="VD: Máy lạnh phòng họp không chạy" />
            </div>
            <div className="field">
              <label>Mô tả chi tiết</label>
              <textarea name="description" rows={3} maxLength={2000}
                placeholder="Mô tả tình trạng, thời điểm phát sinh..." />
            </div>
            <div className="field">
              <label>Họ tên khách hàng *</label>
              <input name="customer_name" required maxLength={100} placeholder="Nguyễn Văn A" />
            </div>
            <div className="field">
              <label>Số điện thoại *</label>
              <input name="customer_phone" required placeholder="0901234567" />
              <div className="hint">Định dạng: 0901234567 hoặc +84901234567 (rào chắn Poka-yoke)</div>
            </div>
            <div className="field">
              <label>Loại yêu cầu *</label>
              <select name="category" defaultValue="khac">
                <option value="ky_thuat">Kỹ thuật</option>
                <option value="thanh_toan">Thanh toán</option>
                <option value="khac">Khác</option>
              </select>
            </div>
            <div className="field">
              <label>Mức ưu tiên (để trống = tự suy luận)</label>
              <select name="priority" defaultValue="">
                <option value="">— Tự động —</option>
                <option value="cao">Cao</option>
                <option value="trung_binh">Trung bình</option>
                <option value="thap">Thấp</option>
              </select>
            </div>
            <button className="btn" type="submit" disabled={loading}>
              {loading ? "Đang gửi..." : "Gửi yêu cầu"}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
