// SPDX-License-Identifier: MIT
"use client";
import Link from "next/link";
import { useState } from "react";
import { Radar } from "./Radar";
import {
  AXIS_META, QUESTIONS, SCALE, scoreAnswers, type Axis, type DiagResult,
} from "./questions";

export default function DiagPage() {
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [result, setResult] = useState<DiagResult | null>(null);

  const answered = Object.keys(answers).length;
  const total = QUESTIONS.length;

  function submit() {
    setResult(scoreAnswers(answers));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <main className="main">
      <div className="container" style={{ paddingTop: 30 }}>
        <Link className="link-back" href="/">← Về trang chủ</Link>

        {result && (
          <div className="panel" style={{ maxWidth: 760, marginBottom: 24 }}>
            <h2>Kết quả chẩn đoán HPDI</h2>
            <p className="sub">
              Mức trưởng thành: <b>{result.level.name}</b> ({result.overall}/100) — {result.level.desc}
            </p>
            <div style={{ display: "flex", gap: 24, flexWrap: "wrap", alignItems: "center" }}>
              <Radar scores={result.scores} />
              <div style={{ flex: 1, minWidth: 240 }}>
                {(["H", "P", "D", "I"] as Axis[]).map((ax) => (
                  <div key={ax} style={{ marginBottom: 10 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, fontWeight: 600 }}>
                      <span style={{ color: AXIS_META[ax].color }}>{AXIS_META[ax].name}</span>
                      <span>{result.scores[ax]}/100</span>
                    </div>
                    <div style={{ height: 8, background: "#eef2f7", borderRadius: 999 }}>
                      <div style={{
                        width: `${result.scores[ax]}%`, height: "100%",
                        background: AXIS_META[ax].color, borderRadius: 999,
                      }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="alert ok" style={{ marginTop: 18 }}>
              <strong>💡 Khuyến nghị (trục yếu nhất: {result.weakest})</strong>
              {result.recommendation}
            </div>
            <button className="btn" onClick={() => { setResult(null); setAnswers({}); }}>
              Làm lại
            </button>
          </div>
        )}

        <div className="panel" style={{ maxWidth: 760 }}>
          <h2>Chẩn đoán độ trưởng thành số (HPDI)</h2>
          <p className="sub">
            Tự "bắt mạch" tổ chức qua {total} câu hỏi trên 4 trục H-P-D-I. Đã trả lời: {answered}/{total}.
          </p>

          {QUESTIONS.map((q, i) => (
            <div className="field" key={i} style={{ borderLeft: `3px solid ${AXIS_META[q.axis].color}`, paddingLeft: 12 }}>
              <label>
                <span style={{ color: AXIS_META[q.axis].color, fontWeight: 700 }}>[{q.axis}]</span> {q.text}
              </label>
              <select
                value={answers[i] ?? ""}
                onChange={(e) => setAnswers({ ...answers, [i]: Number(e.target.value) })}
              >
                <option value="" disabled>— Chọn mức độ —</option>
                {SCALE.map((s) => (
                  <option key={s.value} value={s.value}>{s.value} — {s.label}</option>
                ))}
              </select>
            </div>
          ))}

          <button className="btn" onClick={submit} disabled={answered < total}>
            {answered < total ? `Còn ${total - answered} câu chưa trả lời` : "Xem kết quả chẩn đoán"}
          </button>
        </div>
      </div>
    </main>
  );
}
