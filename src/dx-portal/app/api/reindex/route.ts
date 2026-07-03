// SPDX-License-Identifier: MIT
// Kích hoạt DX-RAG nạp lại tri thức (từ Nextcloud). Chỉ người đã đăng nhập.
import { NextResponse } from "next/server";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/lib/auth";

const DX_RAG_URL = process.env.DX_RAG_URL || "http://localhost:8001";

export async function POST() {
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ message: "Chưa xác thực." }, { status: 401 });
  }
  try {
    const res = await fetch(`${DX_RAG_URL}/ingest`, { method: "POST" });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ message: "Không kết nối được DX-RAG." }, { status: 502 });
  }
}
