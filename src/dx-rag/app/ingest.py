# SPDX-License-Identifier: MIT
"""Nạp tài liệu tri thức [I]: nguồn ưu tiên Nextcloud [H] (WebDAV), fallback thư mục cục bộ.
Luồng: đọc tài liệu → chia đoạn → nhúng → lưu Qdrant.
"""
import glob
import logging
import os
from . import llm, store, webdav

log = logging.getLogger("dx-rag.ingest")
KNOWLEDGE_DIR = os.environ.get("KNOWLEDGE_DIR", "knowledge")


def _chunks(text: str) -> list[str]:
    """Chia theo đoạn (\n\n), bỏ đoạn quá ngắn."""
    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if len(p) >= 30]


async def _load_documents() -> tuple[list[tuple[str, str]], str]:
    """Trả về ([(source, text)], nguồn). Ưu tiên Nextcloud, fallback cục bộ."""
    if webdav.is_configured():
        try:
            hrefs = await webdav.list_markdown()
            docs = [await webdav.fetch(h) for h in hrefs]
            if docs:
                log.info("Nạp %d tài liệu từ Nextcloud", len(docs))
                return docs, "nextcloud"
            log.warning("Nextcloud chưa có tài liệu .md — dùng thư mục cục bộ")
        except Exception as exc:  # Nextcloud lỗi/chưa sẵn sàng → fallback
            log.warning("Không đọc được Nextcloud (%s) — dùng thư mục cục bộ", exc)

    docs = []
    for fp in sorted(glob.glob(f"{KNOWLEDGE_DIR}/*.md")):
        with open(fp, encoding="utf-8") as fh:
            docs.append((os.path.basename(fp), fh.read()))
    return docs, "local"


async def ingest() -> dict:
    documents, source = await _load_documents()
    points: list[dict] = []
    dim = 0
    pid = 0
    for name, text in documents:
        for chunk in _chunks(text):
            vec = await llm.embed(chunk)
            dim = len(vec)
            points.append({"id": pid, "vector": vec,
                           "payload": {"text": chunk, "source": name}})
            pid += 1

    if not points:
        return {"ingested": 0, "files": 0, "source": source}

    # Tạo lại collection để không sót điểm của lần nạp trước (tri thức lỗi thời).
    await store.recreate_collection(dim)
    await store.upsert(points)
    return {"ingested": len(points), "files": len(documents), "dim": dim, "source": source}
