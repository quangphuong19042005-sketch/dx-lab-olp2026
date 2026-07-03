// SPDX-License-Identifier: MIT
// Proxy phía máy chủ: chuyển câu hỏi tới DX-RAG (trợ lý AI nội bộ).
import { NextResponse } from "next/server";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/lib/auth";

const DX_RAG_URL = process.env.DX_RAG_URL || "http://localhost:8001";

export async function POST(req: Request) {
  // Chỉ người đã đăng nhập (SSO) mới được hỏi trợ lý AI (chống lạm dụng quota).
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ message: "Chưa xác thực." }, { status: 401 });
  }
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ message: "Payload không hợp lệ." }, { status: 400 });
  }
  try {
    const res = await fetch(`${DX_RAG_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ message: "Không kết nối được DX-RAG." }, { status: 502 });
  }
}
