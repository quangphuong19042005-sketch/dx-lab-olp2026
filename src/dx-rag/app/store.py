# SPDX-License-Identifier: MIT
"""Kho véc-tơ Qdrant qua REST API (httpx) — không phụ thuộc SDK nặng."""
import httpx
from .config import settings

_base = settings.qdrant_host.rstrip("/")
_col = settings.collection


async def ensure_collection(dim: int) -> None:
    """Tạo collection (khoảng cách cosine) nếu chưa có hoặc sai chiều véc-tơ."""
    async with httpx.AsyncClient(timeout=30) as c:
        info = await c.get(f"{_base}/collections/{_col}")
        if info.status_code == 200:
            size = info.json()["result"]["config"]["params"]["vectors"]["size"]
            if size == dim:
                return
        await c.put(f"{_base}/collections/{_col}",
                    json={"vectors": {"size": dim, "distance": "Cosine"}})


async def upsert(points: list[dict]) -> None:
    """points: [{id, vector, payload}]."""
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.put(f"{_base}/collections/{_col}/points",
                        params={"wait": "true"}, json={"points": points})
        r.raise_for_status()


async def search(vector: list[float], limit: int = 4) -> list[dict]:
    """Trả về top-k payload gần nhất. Kho chưa sẵn sàng → trả rỗng (không ném lỗi)."""
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(f"{_base}/collections/{_col}/points/search",
                         json={"vector": vector, "limit": limit, "with_payload": True})
        if r.status_code == 404:  # collection chưa được tạo
            return []
        r.raise_for_status()
        return r.json()["result"]


async def recreate_collection(dim: int) -> None:
    """Xóa và tạo lại collection — dùng khi ingest để tránh sót điểm cũ."""
    async with httpx.AsyncClient(timeout=30) as c:
        await c.delete(f"{_base}/collections/{_col}")
        await c.put(f"{_base}/collections/{_col}",
                    json={"vectors": {"size": dim, "distance": "Cosine"}})


async def count() -> int:
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(f"{_base}/collections/{_col}/points/count", json={"exact": True})
        if r.status_code != 200:
            return 0
        return r.json()["result"]["count"]
