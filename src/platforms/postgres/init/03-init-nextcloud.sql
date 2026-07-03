-- Cơ sở dữ liệu riêng cho Nextcloud ([H] lưu trữ P.A.R.A).
SELECT 'CREATE DATABASE nextcloud'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nextcloud')\gexec
