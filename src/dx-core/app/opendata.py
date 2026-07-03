# SPDX-License-Identifier: MIT
"""Dữ liệu mở liên kết [D] — xuất ticket ra JSON-LD, CSV và mô tả DCAT.
Kế thừa chủ đề "Dữ liệu mở liên kết" (OLP 2025). Đã ẩn PII (tên/SĐT khách hàng).
"""
import csv
import io

VOCAB = "https://dxlab.opendata.vn/vocab#"

# @context ánh xạ trường dữ liệu sang IRI (tái dùng schema.org + vocab riêng).
CONTEXT = {
    "dx": VOCAB,
    "schema": "http://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "Ticket": "dx:Ticket",
    "title": "schema:name",
    "category": "dx:category",
    "priority": "dx:priority",
    "status": "dx:status",
    "assignee": "dx:assignedTeam",
    "created_at": {"@id": "schema:dateCreated", "@type": "xsd:dateTime"},
    "sla_deadline": {"@id": "dx:slaDeadline", "@type": "xsd:dateTime"},
}

_FIELDS = ["id", "title", "category", "priority", "status", "assignee",
           "created_at", "sla_deadline"]


def _iso(v):
    return v.isoformat() if hasattr(v, "isoformat") else v


def to_jsonld(rows: list[dict]) -> dict:
    """Bọc dữ liệu thành đồ thị JSON-LD liên kết."""
    graph = []
    for r in rows:
        node = {"@id": f"dx:ticket/{r['id']}", "@type": "Ticket"}
        for f in _FIELDS:
            if f == "id":
                continue
            node[f] = _iso(r[f])
        graph.append(node)
    return {"@context": CONTEXT, "@graph": graph}


def to_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=_FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow({f: _iso(r[f]) for f in _FIELDS})
    return buf.getvalue()


def dcat_catalog(base_url: str) -> dict:
    """Mô tả bộ dữ liệu theo chuẩn DCAT (W3C) — catalog dữ liệu mở."""
    return {
        "@context": {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dct": "http://purl.org/dc/terms/",
        },
        "@type": "dcat:Catalog",
        "dct:title": "DX-Lab OSS — Cổng Dữ liệu mở",
        "dct:publisher": "DX-Lab OSS Team",
        "dct:license": "https://opensource.org/licenses/MIT",
        "dcat:dataset": [
            {
                "@type": "dcat:Dataset",
                "dct:identifier": "dx-tickets",
                "dct:title": "Dữ liệu yêu cầu/sự vụ (DX-Ticket)",
                "dct:description": "Ticket đã ẩn thông tin cá nhân, phục vụ phân tích mở.",
                "dcat:keyword": ["ticket", "sla", "hpdi", "dx-os"],
                "dcat:distribution": [
                    {
                        "@type": "dcat:Distribution",
                        "dct:format": "application/ld+json",
                        "dcat:accessURL": f"{base_url}/open-data/tickets.jsonld",
                    },
                    {
                        "@type": "dcat:Distribution",
                        "dct:format": "text/csv",
                        "dcat:accessURL": f"{base_url}/open-data/tickets.csv",
                    },
                ],
            }
        ],
    }
