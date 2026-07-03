-- Tạo cơ sở dữ liệu riêng cho Keycloak (tách khỏi DB nghiệp vụ dxlab).
-- Chạy tự động khi PostgreSQL khởi tạo lần đầu.
SELECT 'CREATE DATABASE keycloak'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'keycloak')\gexec
