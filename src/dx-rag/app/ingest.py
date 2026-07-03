# SPDX-License-Identifier: MIT
"""Nạp tài liệu tri thức [I]: đọc file .md → chia đoạn → nhúng → lưu Qdrant."""
import glob
import os
from . import llm, store

KNOWLEDGE_DIR = os.environ.get("KNOWLEDGE_DIR", "knowledge")


def _chunks(text: str) -> list[str]:
    """Chia theo đoạn (\n\n), bỏ đoạn quá ngắn."""
    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if len(p) >= 30]


async def ingest() -> dict:
    files = sorted(glob.glob(f"{KNOWLEDGE_DIR}/*.md"))
    points: list[dict] = []
    dim = 0
    pid = 0
    for fp in files:
        source = os.path.basename(fp)
        text = open(fp, encoding="utf-8").read()
        for chunk in _chunks(text):
            vec = await llm.embed(chunk)
            dim = len(vec)
            points.append({"id": pid, "vector": vec,
                           "payload": {"text": chunk, "source": source}})
            pid += 1

    if not points:
        return {"ingested": 0, "files": 0}

    await store.ensure_collection(dim)
    await store.upsert(points)
    return {"ingested": len(points), "files": len(files), "dim": dim}
