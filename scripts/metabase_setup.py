#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tự động khởi tạo Metabase cho DX-Lab: tạo admin, kết nối PostgreSQL (SSOT),
dựng dashboard "DX-Ticket" với các biểu đồ đọc dữ liệu ticket thật.

Chạy sau khi Metabase đã healthy:
    python3 scripts/metabase_setup.py
Idempotent ở mức hợp lý: nếu đã setup, script sẽ đăng nhập lại và bỏ qua bước tạo.
"""
import json
import os
import time
import urllib.request
import urllib.error

BASE = os.environ.get("METABASE_URL", "http://localhost:3001")
ADMIN_EMAIL = os.environ.get("MB_ADMIN_EMAIL", "admin@dxlab.local")
ADMIN_PASSWORD = os.environ.get("MB_ADMIN_PASSWORD", "DxLab#2026mb")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "change_me_strong_password")
PG_USER = os.environ.get("POSTGRES_USER", "dxlab")
PG_DB = os.environ.get("POSTGRES_DB", "dxlab")


def api(method, path, body=None, session=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if session:
        req.add_header("X-Metabase-Session", session)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} → {e.code}: {e.read().decode()[:300]}")


def get_session():
    """Setup lần đầu (nếu còn token) hoặc đăng nhập nếu đã setup."""
    props = api("GET", "/api/session/properties")
    token = props.get("setup-token")
    if token:
        print("→ Chạy setup lần đầu (tạo admin + kết nối PostgreSQL)...")
        res = api("POST", "/api/setup", {
            "token": token,
            "user": {
                "first_name": "DX", "last_name": "Admin",
                "email": ADMIN_EMAIL, "password": ADMIN_PASSWORD,
                "site_name": "DX-Lab OSS",
            },
            "prefs": {"site_name": "DX-Lab OSS", "allow_tracking": False},
            "database": {
                "engine": "postgres", "name": "DX-Lab SSOT",
                "details": {
                    "host": "postgres", "port": 5432, "dbname": PG_DB,
                    "user": PG_USER, "password": PG_PASSWORD, "ssl": False,
                },
                "is_full_sync": True,
            },
        })
        return res["id"]
    print("→ Đã setup trước đó, đăng nhập lại...")
    res = api("POST", "/api/session", {"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    return res["id"]


def find_ssot_db(session):
    dbs = api("GET", "/api/database", session=session)
    items = dbs.get("data", dbs) if isinstance(dbs, dict) else dbs
    for d in items:
        if d.get("name") == "DX-Lab SSOT":
            return d["id"]
    # nếu chưa có (đăng nhập lại), tạo mới
    print("→ Chưa có nguồn 'DX-Lab SSOT', tạo kết nối...")
    d = api("POST", "/api/database", {
        "engine": "postgres", "name": "DX-Lab SSOT",
        "details": {"host": "postgres", "port": 5432, "dbname": PG_DB,
                    "user": PG_USER, "password": PG_PASSWORD, "ssl": False},
    }, session=session)
    return d["id"]


def wait_for_table(session, db_id, table="tickets", tries=30):
    """Chờ Metabase quét xong schema để thấy bảng tickets."""
    api("POST", f"/api/database/{db_id}/sync_schema", session=session)
    for _ in range(tries):
        meta = api("GET", f"/api/database/{db_id}/metadata", session=session)
        for t in meta.get("tables", []):
            if t["name"] == table:
                print(f"→ Đã thấy bảng '{table}' (id={t['id']})")
                return t["id"]
        time.sleep(2)
    raise RuntimeError(f"Không thấy bảng {table} sau khi sync")


def make_card(session, db_id, name, sql, display, viz=None):
    card = api("POST", "/api/card", {
        "name": name,
        "display": display,
        "dataset_query": {
            "type": "native",
            "native": {"query": sql, "template-tags": {}},
            "database": db_id,
        },
        "visualization_settings": viz or {},
    }, session=session)
    print(f"  ✓ Card: {name} (id={card['id']})")
    return card["id"]


def main():
    session = get_session()
    db_id = find_ssot_db(session)
    wait_for_table(session, db_id, "tickets")

    print("→ Tạo các biểu đồ...")
    cards = []
    cards.append((make_card(session, db_id, "Tổng số ticket",
        "SELECT count(*) AS tong FROM tickets", "scalar"), 0, 0, 4, 3))
    cards.append((make_card(session, db_id, "Đang quá hạn SLA",
        "SELECT count(*) AS qua_han FROM tickets "
        "WHERE sla_deadline < now() AND status NOT IN ('hoan_thanh','da_huy')",
        "scalar"), 0, 4, 4, 3))
    cards.append((make_card(session, db_id, "Tỷ lệ hoàn thành",
        "SELECT round(100.0*count(*) FILTER (WHERE status='hoan_thanh')/count(*),1) AS ty_le "
        "FROM tickets", "scalar"), 0, 8, 4, 3))
    cards.append((make_card(session, db_id, "Ticket theo loại",
        "SELECT category AS loai, count(*) AS so_luong FROM tickets GROUP BY 1 ORDER BY 2 DESC",
        "pie"), 3, 0, 6, 5))
    cards.append((make_card(session, db_id, "Ticket theo trạng thái",
        "SELECT status AS trang_thai, count(*) AS so_luong FROM tickets GROUP BY 1 ORDER BY 2 DESC",
        "row"), 3, 6, 6, 5))
    cards.append((make_card(session, db_id, "Ticket theo mức ưu tiên",
        "SELECT priority AS uu_tien, count(*) AS so_luong FROM tickets GROUP BY 1 ORDER BY 2 DESC",
        "bar"), 8, 0, 6, 5))
    cards.append((make_card(session, db_id, "Xu hướng ticket theo ngày",
        "SELECT date_trunc('day', created_at)::date AS ngay, count(*) AS so_luong "
        "FROM tickets GROUP BY 1 ORDER BY 1", "line"), 8, 6, 6, 5))

    print("→ Tạo dashboard...")
    dash = api("POST", "/api/dashboard", {
        "name": "DX-Ticket — Bảng điều khiển vận hành",
        "description": "Giám sát thời gian thực yêu cầu khách hàng (không gian [D]).",
    }, session=session)
    dash_id = dash["id"]

    dashcards = [{
        "id": -(i + 1), "card_id": cid,
        "row": row, "col": col, "size_x": sx, "size_y": sy,
    } for i, (cid, row, col, sx, sy) in enumerate(cards)]
    api("PUT", f"/api/dashboard/{dash_id}", {"dashcards": dashcards}, session=session)

    print(f"\n✅ HOÀN TẤT — Mở dashboard tại: {BASE}/dashboard/{dash_id}")
    print(f"   Đăng nhập: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    main()
