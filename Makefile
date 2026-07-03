# DX-Lab OSS — Task runner
# Dùng: make <target>. Xem `make help`.

.PHONY: help init up down logs ps restart clean

help: ## Hiện danh sách lệnh
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

init: ## Tạo file .env từ mẫu (nếu chưa có)
	@test -f .env || (cp .env.example .env && echo "Đã tạo .env — hãy sửa mật khẩu trước khi chạy!")

up: init ## Dựng toàn bộ hệ thống (nền)
	docker compose up -d

down: ## Dừng hệ thống
	docker compose down

logs: ## Xem log realtime
	docker compose logs -f

ps: ## Trạng thái các service
	docker compose ps

restart: ## Khởi động lại
	docker compose restart

clean: ## Dừng và XÓA volume dữ liệu (cẩn thận!)
	docker compose down -v
