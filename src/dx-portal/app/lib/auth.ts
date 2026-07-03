// SPDX-License-Identifier: MIT
// Cấu hình next-auth ↔ Keycloak (OIDC). wellKnown trỏ keycloak:8080 (backchannel
// nội bộ), issuer = localhost:8080 (khớp iss token do trình duyệt đăng nhập).
import type { NextAuthOptions } from "next-auth";
import KeycloakProvider from "next-auth/providers/keycloak";

export const authOptions: NextAuthOptions = {
  providers: [
    KeycloakProvider({
      clientId: process.env.KEYCLOAK_ID ?? "dx-portal",
      clientSecret: process.env.KEYCLOAK_SECRET ?? "",
      issuer: process.env.KEYCLOAK_ISSUER,
      wellKnown: process.env.KEYCLOAK_WELLKNOWN,
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  session: { strategy: "jwt" },
};
