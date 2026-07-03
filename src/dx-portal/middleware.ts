// SPDX-License-Identifier: MIT
// Bảo vệ mọi trang: chưa đăng nhập → chuyển tới Keycloak (SSO). Loại trừ API & tài nguyên tĩnh.
export { default } from "next-auth/middleware";

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
