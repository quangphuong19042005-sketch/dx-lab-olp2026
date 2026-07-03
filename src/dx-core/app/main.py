# SPDX-License-Identifier: MIT
"""DX-Core API — điểm vào trục sự kiện.

Luồng: biểu mẫu [P] → webhook → chuẩn hóa (Poka-yoke) → rule engine (phân công + SLA)
       → ghi PostgreSQL [D] → cảnh báo Telegram [H].
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from . import db, rules
from .models import Ticket, TicketIn
from .notify import send_alert

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.pool.open()
    await db.init_schema()
    yield
    await db.pool.close()


app = FastAPI(title="DX-Core — Event Bus", version="0.2.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "dx-core"}


@app.post("/webhooks/ticket", response_model=Ticket, status_code=201)
async def receive_ticket(payload: TicketIn) -> Ticket:
    """Tiếp nhận ticket mới từ [P], áp quy tắc, lưu trữ và cảnh báo."""
    now = datetime.now(timezone.utc)
    priority = rules.infer_priority(payload)
    assignee = rules.assign(payload)
    deadline = rules.sla_deadline(priority, now)

    row = await db.insert_ticket(
        payload.model_dump(mode="json"), assignee, priority.value, deadline
    )

    await send_alert(
        f"🎫 <b>Ticket mới #{row['id']}</b>\n"
        f"• {row['title']}\n"
        f"• Khách: {row['customer_name']} ({row['customer_phone']})\n"
        f"• Ưu tiên: {priority.value} → giao <b>{assignee}</b>\n"
        f"• Hạn SLA: {deadline:%d/%m %H:%M}"
    )
    return Ticket(**row)
