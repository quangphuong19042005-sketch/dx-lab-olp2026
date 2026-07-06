# SPDX-License-Identifier: MIT
"""Đọc & khởi tạo tài liệu tri thức [H] trên Nextcloud qua WebDAV (không phụ thuộc SDK)."""
import asyncio
import glob
import logging
import os
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import httpx
from .config import settings

log = logging.getLogger("dx-rag.webdav")

_PARA = ["DX-Lab", "DX-Lab/1-Projects", "DX-Lab/2-Areas",
         "DX-Lab/3-Resources", "DX-Lab/4-Archives"]


def _base() -> str:
    root = settings.nextcloud_url.rstrip("/")
    return f"{root}/remote.php/dav/files/{settings.nextcloud_user}"


def _auth():
    return (settings.nextcloud_user, settings.nextcloud_password)


def is_configured() -> bool:
    return bool(settings.nextcloud_url and settings.nextcloud_user and settings.nextcloud_password)


async def wait_ready(tries: int = 60, delay: float = 5) -> bool:
    """Chờ Nextcloud cài xong (status.php báo installed:true)."""
    url = f"{settings.nextcloud_url.rstrip('/')}/status.php"
    for _ in range(tries):
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(url)
                if r.status_code == 200 and '"installed":true' in r.text:
                    return True
        except Exception:
            pass
        await asyncio.sleep(delay)
    return False


async def seed_if_empty(local_dir: str) -> bool:
    """Nếu kho tri thức trên Nextcloud chưa có .md → tạo cấu trúc P.A.R.A và tải
    tài liệu SOP mẫu (đóng gói sẵn trong image) lên. Tự động hóa cho 'một lệnh'."""
    try:
        if await list_markdown():
            return False  # đã có tài liệu, không seed
    except Exception:
        pass  # thư mục chưa tồn tại → sẽ tạo bên dưới
    kpath = settings.nextcloud_knowledge_path.strip("/")
    files = sorted(glob.glob(f"{local_dir}/*.md"))
    async with httpx.AsyncClient(timeout=30, auth=_auth()) as c:
        for folder in _PARA:
            await c.request("MKCOL", f"{_base()}/{folder}")  # 201/405 đều chấp nhận
        for fp in files:
            with open(fp, encoding="utf-8") as fh:
                await c.put(f"{_base()}/{kpath}/{os.path.basename(fp)}",
                            content=fh.read().encode("utf-8"))
    log.info("Đã khởi tạo P.A.R.A + tải %d tài liệu SOP lên Nextcloud", len(files))
    return True


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
