-- SPDX-License-Identifier: MIT
-- Dữ liệu mẫu DX-Ticket cho demo dashboard [D]. Idempotent: xóa dữ liệu seed cũ trước.
-- Chạy: docker exec -i dxlab-postgres psql -U dxlab -d dxlab < seed/seed_tickets.sql

DELETE FROM tickets WHERE description LIKE 'SEED:%';

-- CTE gắn với generate_series → random() được tính RIÊNG cho từng dòng.
WITH gen AS (
    SELECT
        g,
        (ARRAY['ky_thuat','thanh_toan','khac'])[1 + floor(random()*3)]                       AS cat,
        (ARRAY['cao','trung_binh','thap'])[1 + floor(random()*3)]                            AS pri,
        (ARRAY['moi','dang_xu_ly','hoan_thanh','hoan_thanh','hoan_thanh','da_huy'])[1 + floor(random()*6)] AS st,
        now() - (random() * interval '30 days')                                             AS created
    FROM generate_series(1, 40) AS g
)
INSERT INTO tickets
    (title, description, customer_name, customer_phone,
     category, priority, assignee, status, sla_deadline, created_at)
SELECT
    (ARRAY['Máy lạnh không chạy','Yêu cầu bảo hành thiết bị','Wifi chập chờn',
           'Sai hóa đơn tháng','Yêu cầu hoàn tiền','Đổi trả sản phẩm lỗi',
           'Cần hỗ trợ cài đặt','Khiếu nại thái độ phục vụ','Tư vấn gói dịch vụ',
           'Lỗi đăng nhập ứng dụng'])[1 + floor(random()*10)]::text,
    'SEED: nội dung yêu cầu mẫu #' || g,
    (ARRAY['Nguyễn Văn An','Trần Thị Bình','Lê Văn Cường','Phạm Thị Dung',
           'Hoàng Văn Em','Vũ Thị Phương','Đặng Văn Giang','Bùi Thị Hoa'])[1 + floor(random()*8)],
    '09' || lpad((floor(random()*100000000))::bigint::text, 8, '0'),
    cat,
    pri,
    CASE cat WHEN 'ky_thuat' THEN 'to-ky-thuat'
             WHEN 'thanh_toan' THEN 'to-ke-toan'
             ELSE 'to-cskh' END,
    st,
    created + (CASE pri WHEN 'cao' THEN interval '4 hours'
                        WHEN 'trung_binh' THEN interval '24 hours'
                        ELSE interval '72 hours' END),
    created
FROM gen;

SELECT category, priority, count(*) AS so_luong
FROM tickets GROUP BY 1,2 ORDER BY 1,2;
