# SPDX-License-Identifier: MIT
"""Đọc tài liệu tri thức [H] từ Nextcloud qua WebDAV (không phụ thuộc SDK)."""
import logging
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import httpx
from .config import settings

log = logging.getLogger("dx-rag.webdav")


def _base() -> str:
    root = settings.nextcloud_url.rstrip("/")
    return f"{root}/remote.php/dav/files/{settings.nextcloud_user}"


def is_configured() -> bool:
    return bool(settings.nextcloud_url and settings.nextcloud_user and settings.nextcloud_password)


async def list_markdown() -> list[str]:
    """Liệt kê đường dẫn file .md trong thư mục tri thức (PROPFIND, Depth 1)."""
    url = f"{_base()}/{settings.nextcloud_knowledge_path.strip('/')}/"
    auth = (settings.nextcloud_user, settings.nextcloud_password)
    async with httpx.AsyncClient(timeout=30, auth=auth) as c:
        r = await c.request("PROPFIND", url, headers={"Depth": "1"})
        r.raise_for_status()
    root = ET.fromstring(r.text)
    hrefs = []
    for href in root.iter("{DAV:}href"):
        path = unquote(href.text or "")
        if path.lower().endswith(".md"):
            hrefs.append(path)
    return hrefs


async def fetch(href: str) -> tuple[str, str]:
    """Tải nội dung 1 file; trả về (tên_file, nội_dung)."""
    root = settings.nextcloud_url.rstrip("/")
    url = f"{root}{href}"
    auth = (settings.nextcloud_user, settings.nextcloud_password)
    async with httpx.AsyncClient(timeout=30, auth=auth) as c:
        r = await c.get(url)
        r.raise_for_status()
    name = href.rstrip("/").split("/")[-1]
    return name, r.text
