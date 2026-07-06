// SPDX-License-Identifier: MIT
import { describe, it, expect } from "vitest";
import { scoreAnswers, QUESTIONS } from "./questions";

describe("scoreAnswers — chấm điểm trưởng thành HPDI", () => {
  it("có đúng 12 câu, 3 câu mỗi trục", () => {
    expect(QUESTIONS.length).toBe(12);
    for (const ax of ["H", "P", "D", "I"] as const) {
      expect(QUESTIONS.filter((q) => q.axis === ax).length).toBe(3);
    }
  });

  it("tất cả 0 → điểm 0, mức Khởi động", () => {
    const r = scoreAnswers({});
    expect(r.overall).toBe(0);
    expect(r.scores.H).toBe(0);
    expect(r.level.name).toBe("Khởi động");
  });

  it("tất cả 4 → điểm 100, mức Tối ưu", () => {
    const ans: Record<number, number> = {};
    for (let i = 0; i < 12; i++) ans[i] = 4;
    const r = scoreAnswers(ans);
    expect(r.overall).toBe(100);
    expect(r.level.name).toBe("Tối ưu");
  });

  it("khuyến nghị trục yếu ĐẦU TIÊN theo thứ tự H→P→D→I", () => {
    // H mạnh (100), P yếu (0), D vừa (50), I thấp (25) → ưu tiên P (yếu đầu tiên < 50)
    const ans: Record<number, number> = {
      0: 4, 1: 4, 2: 4, 3: 0, 4: 0, 5: 0, 6: 2, 7: 2, 8: 2, 9: 1, 10: 1, 11: 1,
    };
    const r = scoreAnswers(ans);
    expect(r.scores.H).toBe(100);
    expect(r.scores.P).toBe(0);
    expect(r.weakest).toBe("P");
    expect(r.recommendation).toContain("[P]");
  });
});
