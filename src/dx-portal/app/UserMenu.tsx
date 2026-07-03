// SPDX-License-Identifier: MIT
"use client";
import { useSession, signOut } from "next-auth/react";

export function UserMenu() {
  const { data } = useSession();
  const name = data?.user?.name || data?.user?.email;
  if (!name) return null;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <span style={{ fontSize: 13, color: "#cbd5e1" }}>👤 {name}</span>
      <button
        onClick={() => signOut({ callbackUrl: "/" })}
        style={{
          background: "rgba(255,255,255,.12)", color: "#fff", border: "1px solid rgba(255,255,255,.25)",
          padding: "6px 12px", borderRadius: 8, fontSize: 13, cursor: "pointer",
        }}
      >
        Đăng xuất
      </button>
    </div>
  );
}
