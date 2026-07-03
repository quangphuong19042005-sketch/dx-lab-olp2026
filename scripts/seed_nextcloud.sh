#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Khởi tạo cấu trúc lưu trữ P.A.R.A trên Nextcloud [H] và nạp tài liệu SOP mẫu.
# Chạy sau khi Nextcloud đã cài xong:  bash scripts/seed_nextcloud.sh
set -euo pipefail

NC_PORT="${NEXTCLOUD_PORT:-8090}"
NC_USER="${NEXTCLOUD_ADMIN_USER:-admin}"
NC_PASS="${NEXTCLOUD_ADMIN_PASSWORD:?Cần NEXTCLOUD_ADMIN_PASSWORD (nạp .env trước)}"
DAV="http://localhost:${NC_PORT}/remote.php/dav/files/${NC_USER}"
AUTH="${NC_USER}:${NC_PASS}"
KDIR="$(dirname "$0")/../src/dx-rag/knowledge"

echo "→ Tạo cấu trúc P.A.R.A..."
for d in "DX-Lab" "DX-Lab/1-Projects" "DX-Lab/2-Areas" "DX-Lab/3-Resources" "DX-Lab/4-Archives"; do
  curl -s -o /dev/null -u "$AUTH" -X MKCOL "$DAV/$d" || true
done

echo "→ Nạp tài liệu SOP vào 3-Resources..."
for f in "$KDIR"/*.md; do
  name="$(basename "$f")"
  code="$(curl -s -o /dev/null -w '%{http_code}' -u "$AUTH" -T "$f" "$DAV/DX-Lab/3-Resources/$name")"
  echo "   $name → $code"
done
echo "✅ Xong. Kích hoạt nạp tri thức: curl -X POST http://localhost:8001/ingest"
