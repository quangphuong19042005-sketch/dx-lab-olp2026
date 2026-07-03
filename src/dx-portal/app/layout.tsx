// SPDX-License-Identifier: MIT
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DX-Portal — DX-Lab OSS",
  description: "Cổng thông tin nội bộ: nguồn sự thật duy nhất của hệ điều hành doanh nghiệp số.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
