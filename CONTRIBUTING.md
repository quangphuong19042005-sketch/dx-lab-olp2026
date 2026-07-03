# Hướng dẫn đóng góp — DX-Lab OSS

Cảm ơn bạn quan tâm đến DX-Lab OSS! Dự án hoan nghênh mọi đóng góp từ cộng đồng nguồn mở.

## Quy trình đóng góp

1. **Fork** kho mã và tạo nhánh từ `main`: `git checkout -b feat/ten-tinh-nang`.
2. Cài đặt môi trường phát triển theo [README](README.md#bắt-đầu-nhanh-quickstart).
3. Viết code + kiểm thử. Bảo đảm pre-commit hooks chạy sạch.
4. Commit theo chuẩn **Conventional Commits** (xem dưới).
5. Mở **Pull Request** vào `main`, mô tả rõ thay đổi và liên kết Issue liên quan.

## Chuẩn commit (Conventional Commits)

```
<type>(<scope>): <mô tả ngắn>
```

- `type`: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`.
- `scope`: `dx-core`, `dx-portal`, `dx-diag`, `dx-rag`, `platforms`, `docs`...
- Ví dụ: `feat(dx-core): thêm event bus định tuyến ticket`.

## Quy tắc mã nguồn

- **Mỗi tệp mã tự viết phải có header giấy phép SPDX**: `SPDX-License-Identifier: MIT`.
- **Không chỉnh sửa mã nguồn của nền tảng/thư viện bên thứ ba** — chỉ cấu hình qua file ngoài.
- Python: định dạng bằng `ruff`/`black`. JS/TS: `biome`/`prettier`.
- Mọi tính năng phải truy vết được về một pain point trong `docs/du-an.md`.

## Báo lỗi & đề xuất

Dùng [GitHub Issues](../../issues) với đúng mẫu (bug / feature request).

## Giấy phép đóng góp

Khi gửi đóng góp, bạn đồng ý phát hành nó theo giấy phép [MIT](LICENSE) của dự án.
