// SPDX-License-Identifier: MIT
"use client";
import { Axis, AXIS_META } from "./questions";

const ORDER: Axis[] = ["H", "P", "D", "I"];

/** Biểu đồ radar 4 trục H-P-D-I vẽ bằng SVG thuần. */
export function Radar({ scores }: { scores: Record<Axis, number> }) {
  const size = 300;
  const c = size / 2;
  const r = c - 46;
  // 4 trục: trên (H), phải (P), dưới (D), trái (I).
  const angle = (i: number) => (Math.PI / 2) * i - Math.PI / 2;
  const point = (i: number, val: number) => {
    const rad = (val / 100) * r;
    return [c + rad * Math.cos(angle(i)), c + rad * Math.sin(angle(i))];
  };

  const rings = [25, 50, 75, 100];
  const dataPts = ORDER.map((ax, i) => point(i, scores[ax]).join(",")).join(" ");

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} role="img" aria-label="Biểu đồ radar HPDI">
      {rings.map((ring) => (
        <polygon
          key={ring}
          points={ORDER.map((_, i) => point(i, ring).join(",")).join(" ")}
          fill="none" stroke="#e2e8f0" strokeWidth={1}
        />
      ))}
      {ORDER.map((_, i) => {
        const [x, y] = point(i, 100);
        return <line key={i} x1={c} y1={c} x2={x} y2={y} stroke="#e2e8f0" strokeWidth={1} />;
      })}
      <polygon points={dataPts} fill="rgba(37,99,235,.18)" stroke="#2563eb" strokeWidth={2} />
      {ORDER.map((ax, i) => {
        const [x, y] = point(i, scores[ax]);
        return <circle key={ax} cx={x} cy={y} r={4} fill={AXIS_META[ax].color} />;
      })}
      {ORDER.map((ax, i) => {
        const [x, y] = point(i, 122);
        return (
          <text key={ax} x={x} y={y} textAnchor="middle" dominantBaseline="middle"
            fontSize={13} fontWeight={700} fill={AXIS_META[ax].color}>
            {ax} · {scores[ax]}
          </text>
        );
      })}
    </svg>
  );
}
