# Chính sách Bảo mật

## Phạm vi

Chính sách này áp dụng cho mã nguồn tự viết của DX-Lab OSS (`src/dx-core`, `src/dx-portal`,
`src/dx-diag`, `src/dx-rag`) và cấu hình triển khai. Lỗ hổng của các nền tảng bên thứ ba
(Keycloak, Nextcloud, Baserow...) xin báo cáo trực tiếp cho dự án upstream tương ứng.

## Báo cáo lỗ hổng

Nếu phát hiện lỗ hổng bảo mật, **vui lòng KHÔNG mở Issue công khai**. Thay vào đó:

1. Gửi mô tả chi tiết (bước tái hiện, ảnh hưởng, phiên bản) qua kênh riêng của nhóm phát triển.
2. Cho chúng tôi thời gian hợp lý để vá trước khi công bố.

Chúng tôi sẽ phản hồi trong thời gian sớm nhất và ghi nhận đóng góp của bạn.

## Thực hành bảo mật trong dự án

- Mọi bí mật (mật khẩu, token, khóa) đặt trong `.env` — **không bao giờ commit**.
- Định danh tập trung qua Keycloak (OIDC), cơ chế "cắt quyền một chạm".
- Nguyên tắc đặc quyền tối thiểu cho từng service.
- Quét bí mật trước khi push (pre-commit).
