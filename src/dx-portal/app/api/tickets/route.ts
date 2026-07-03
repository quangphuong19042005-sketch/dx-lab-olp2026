// SPDX-License-Identifier: MIT
// Proxy phía máy chủ: chuyển tiếp form ticket tới DX-Core (tránh CORS, ẩn URL nội bộ).
import { NextResponse } from "next/server";

const DX_CORE_URL = process.env.DX_CORE_URL || "http://localhost:8000";

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ message: "Payload không hợp lệ." }, { status: 400 });
  }

  try {
    const res = await fetch(`${DX_CORE_URL}/webhooks/ticket`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();

    if (res.ok) return NextResponse.json(data, { status: 201 });

    // 422 từ Poka-yoke → trích thông điệp lỗi đầu tiên cho thân thiện.
    let message = "Dữ liệu không hợp lệ.";
    if (Array.isArray(data?.detail) && data.detail[0]?.msg) {
      message = data.detail[0].msg.replace(/^Value error,\s*/, "");
    }
    return NextResponse.json({ message }, { status: res.status });
  } catch {
    return NextResponse.json(
      { message: "Không kết nối được DX-Core." },
      { status: 502 }
    );
  }
}
