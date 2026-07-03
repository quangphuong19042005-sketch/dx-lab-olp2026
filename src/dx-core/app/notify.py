# SPDX-License-Identifier: MIT
"""Kênh cảnh báo [H] — bắn thông báo ticket mới vào Telegram (nếu cấu hình)."""
import logging
import httpx
from .config import settings

log = logging.getLogger("dx-core.notify")


async def send_alert(text: str) -> bool:
    """Gửi cảnh báo tới Telegram. Nếu chưa cấu hình token thì chỉ ghi log."""
    if not settings.telegram_bot_token or not settings.telegram_alert_chat_id:
        log.info("[ALERT — chưa cấu hình Telegram] %s", text)
        return False
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                url,
                json={
                    "chat_id": settings.telegram_alert_chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
            )
            resp.raise_for_status()
        return True
    except httpx.HTTPError as exc:  # không để lỗi kênh phụ làm hỏng luồng chính
        log.warning("Gửi Telegram thất bại: %s", exc)
        return False
