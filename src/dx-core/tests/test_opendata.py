# SPDX-License-Identifier: MIT
"""Unit test cho tầng dữ liệu mở liên kết [D] — thuần, không cần DB."""
from datetime import datetime, timezone
from app import opendata

_ROWS = [{
    "id": 1, "title": "Lỗi 500 & timeout <urgent>", "category": "ky_thuat",
    "priority": "cao", "status": "moi", "assignee": "to-ky-thuat",
    "created_at": datetime(2026, 7, 3, tzinfo=timezone.utc),
    "sla_deadline": datetime(2026, 7, 3, 4, tzinfo=timezone.utc),
}]


def test_jsonld_co_context_va_graph():
    d = opendata.to_jsonld(_ROWS)
    assert "@context" in d and "@graph" in d
    node = d["@graph"][0]
    assert node["@id"] == "dx:ticket/1"
    assert node["@type"] == "Ticket"
    assert node["title"] == "Lỗi 500 & timeout <urgent>"
    assert node["created_at"] == "2026-07-03T00:00:00+00:00"
    assert "id" not in node  # id chỉ nằm ở @id


def test_khong_lo_pii():
    js = str(opendata.to_jsonld(_ROWS))
    csv = opendata.to_csv(_ROWS)
    for blob in (js, csv):
        assert "customer" not in blob.lower()
        assert "phone" not in blob.lower()


def test_csv_header_va_dong():
    lines = opendata.to_csv(_ROWS).strip().splitlines()
    assert lines[0].startswith("id,title,category")
    assert "to-ky-thuat" in lines[1]


def test_dcat_catalog_hop_le():
    c = opendata.dcat_catalog("http://host:8000")
    assert c["@type"] == "dcat:Catalog"
    dist = c["dcat:dataset"][0]["dcat:distribution"]
    formats = {d["dct:format"] for d in dist}
    assert "application/ld+json" in formats
    assert "text/csv" in formats
    assert dist[0]["dcat:accessURL"].startswith("http://host:8000/open-data/")
