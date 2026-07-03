-- Tạo cơ sở dữ liệu riêng cho Metabase (app database của BI tool).
-- Chạy tự động khi PostgreSQL khởi tạo lần đầu.
SELECT 'CREATE DATABASE metabase'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'metabase')\gexec
