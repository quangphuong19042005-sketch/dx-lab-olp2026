// SPDX-License-Identifier: MIT
// Đường dẫn các dịch vụ trong hệ sinh thái DX-Lab (client-side → dùng origin trình duyệt).
export const links = {
  metabase: process.env.NEXT_PUBLIC_METABASE_URL || "http://localhost:3001/dashboard/2",
  keycloak: process.env.NEXT_PUBLIC_KEYCLOAK_URL || "http://localhost:8080",
  dxCoreDocs: process.env.NEXT_PUBLIC_DX_CORE_URL || "http://localhost:8000/docs",
  baserow: process.env.NEXT_PUBLIC_BASEROW_URL || "http://localhost:8085",
};
