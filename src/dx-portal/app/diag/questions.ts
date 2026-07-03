// SPDX-License-Identifier: MIT
// Ngân hàng câu hỏi chẩn đoán độ trưởng thành HPDI (DTI) + logic chấm điểm.
// Bám giáo trình DX-OS chương 2 (khung DTI) và triết lý H-P-D-I.

export type Axis = "H" | "P" | "D" | "I";

export interface Question {
  axis: Axis;
  text: string;
}

export const AXIS_META: Record<Axis, { name: string; color: string; hint: string }> = {
  H: { name: "[H] Con người", color: "#4338ca", hint: "Định danh, lưu trữ P.A.R.A, cổng thông tin, giao tiếp chuẩn hóa" },
  P: { name: "[P] Quy trình", color: "#0e7490", hint: "Số hóa luồng việc, rào chắn Poka-yoke, tự động hóa" },
  D: { name: "[D] Dữ liệu", color: "#15803d", hint: "Nguồn sự thật duy nhất, dashboard thời gian thực" },
  I: { name: "[I] Trí tuệ", color: "#a21caf", hint: "AI bám tri thức nội bộ, tác tử tự hành" },
};

// Thang trả lời chung: 0 = chưa có → 4 = đã tối ưu.
export const SCALE = [
  { value: 0, label: "Chưa có / thủ công hoàn toàn" },
  { value: 1, label: "Sơ khai, rời rạc" },
  { value: 2, label: "Có nhưng chưa chuẩn hóa" },
  { value: 3, label: "Chuẩn hóa, dùng đều" },
  { value: 4, label: "Tối ưu, tự động" },
];

export const QUESTIONS: Question[] = [
  { axis: "H", text: "Nhân sự dùng một tài khoản định danh tập trung (SSO) để vào mọi công cụ?" },
  { axis: "H", text: "Tài liệu được lưu trữ theo cấu trúc thống nhất (vd: P.A.R.A), tìm là thấy?" },
  { axis: "H", text: "Có một cổng thông tin/nguồn sự thật duy nhất để bắt đầu công việc?" },

  { axis: "P", text: "Các quy trình chính được số hóa thành luồng việc (không chạy bằng trí nhớ)?" },
  { axis: "P", text: "Biểu mẫu nhập liệu có rào chắn chống sai (Poka-yoke) ngay đầu nguồn?" },
  { axis: "P", text: "Việc chuyển giao giữa các bộ phận được tự động hóa (không nhắn tin thủ công)?" },

  { axis: "D", text: "Dữ liệu tập trung về một nguồn sự thật duy nhất (không mỗi nơi một Excel)?" },
  { axis: "D", text: "Lãnh đạo xem được bảng điều khiển số liệu thời gian thực?" },
  { axis: "D", text: "Quyết định dựa trên số liệu định lượng thay vì cảm tính/báo cáo cuối tháng?" },

  { axis: "I", text: "Có trợ lý AI trả lời dựa trên tài liệu nội bộ (không bịa/ảo giác)?" },
  { axis: "I", text: "AI được tích hợp vào quy trình để tự phân loại/định tuyến công việc?" },
  { axis: "I", text: "Hệ thống tự động cảnh báo/đề xuất hành động mà không cần thao tác tay?" },
];

export const LEVELS = [
  { min: 0, name: "Khởi động", desc: "Vận hành thủ công, rủi ro rác dữ liệu cao." },
  { min: 25, name: "Hình thành", desc: "Bắt đầu số hóa nhưng chưa đồng bộ." },
  { min: 50, name: "Chuẩn hóa", desc: "Quy trình & dữ liệu đã có kỷ luật." },
  { min: 75, name: "Tối ưu", desc: "Vận hành bằng dữ liệu, tiến tới tự hành AI." },
];

export interface DiagResult {
  scores: Record<Axis, number>; // 0-100 mỗi trục
  overall: number;
  level: { name: string; desc: string };
  weakest: Axis;
  recommendation: string;
}

/** Chấm điểm: trung bình mỗi trục, chuẩn hóa về 0-100. */
export function scoreAnswers(answers: Record<number, number>): DiagResult {
  const byAxis: Record<Axis, number[]> = { H: [], P: [], D: [], I: [] };
  QUESTIONS.forEach((q, i) => byAxis[q.axis].push(answers[i] ?? 0));

  const scores = {} as Record<Axis, number>;
  (Object.keys(byAxis) as Axis[]).forEach((ax) => {
    const arr = byAxis[ax];
    const avg = arr.reduce((s, v) => s + v, 0) / arr.length;
    scores[ax] = Math.round((avg / 4) * 100);
  });

  const order: Axis[] = ["H", "P", "D", "I"];
  const overall = Math.round(order.reduce((s, a) => s + scores[a], 0) / 4);
  const level = [...LEVELS].reverse().find((l) => overall >= l.min) ?? LEVELS[0];

  // Nguyên lý HPDI tuyến tính: vá từ gốc. Trục cần ưu tiên = trục ĐẦU TIÊN
  // (theo thứ tự H→P→D→I) còn dưới ngưỡng 50; nếu mọi trục đều ổn, lấy trục thấp nhất.
  const GATE = 50;
  let weakest = order.find((a) => scores[a] < GATE);
  if (!weakest) {
    weakest = order.reduce((lo, a) => (scores[a] < scores[lo] ? a : lo), order[0]);
  }
  const recMap: Record<Axis, string> = {
    H: "Ưu tiên nền móng [H]: thiết lập SSO, chuẩn hóa lưu trữ P.A.R.A và cổng thông tin nội bộ trước khi tự động hóa.",
    P: "Củng cố [P]: số hóa quy trình lõi, cài rào chắn Poka-yoke để chặn rác đầu vào rồi mới nói tới dữ liệu sạch.",
    D: "Tập trung [D]: gom về nguồn sự thật duy nhất và dựng dashboard thời gian thực trước khi triển khai AI.",
    I: "Sẵn sàng cho [I]: dữ liệu đã sạch — có thể nhúng AI bám tri thức nội bộ và tác tử tự hành.",
  };

  return { scores, overall, level, weakest, recommendation: recMap[weakest] };
}
