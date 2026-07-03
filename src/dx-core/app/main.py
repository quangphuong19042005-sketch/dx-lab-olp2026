# SPDX-License-Identifier: MIT
"""DX-Core API — điểm vào trục sự kiện.

Luồng: biểu mẫu [P] → webhook → chuẩn hóa (Poka-yoke) → rule engine (phân công + SLA)
       → ghi PostgreSQL [D] → cảnh báo Telegram [H].
"""
import html
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from . import db, opendata, rules
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


@app.get("/open-data/catalog.jsonld", tags=["open-data"])
async def od_catalog(request: Request) -> JSONResponse:
    """Danh mục dữ liệu mở (DCAT)."""
    base = str(request.base_url).rstrip("/")
    return JSONResponse(opendata.dcat_catalog(base), media_type="application/ld+json")


@app.get("/open-data/context.jsonld", tags=["open-data"])
async def od_context() -> JSONResponse:
    return JSONResponse({"@context": opendata.CONTEXT}, media_type="application/ld+json")


@app.get("/open-data/tickets.jsonld", tags=["open-data"])
async def od_tickets_jsonld() -> JSONResponse:
    """Ticket dạng JSON-LD liên kết (đã ẩn PII)."""
    rows = await db.list_public_tickets()
    return JSONResponse(opendata.to_jsonld(rows), media_type="application/ld+json")


@app.get("/open-data/tickets.csv", tags=["open-data"])
async def od_tickets_csv() -> Response:
    rows = await db.list_public_tickets()
    return Response(opendata.to_csv(rows), media_type="text/csv")


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

    # Escape các trường người dùng vì gửi Telegram ở chế độ parse_mode=HTML.
    await send_alert(
        f"🎫 <b>Ticket mới #{row['id']}</b>\n"
        f"• {html.escape(row['title'])}\n"
        f"• Khách: {html.escape(row['customer_name'])} ({html.escape(row['customer_phone'])})\n"
        f"• Ưu tiên: {priority.value} → giao <b>{assignee}</b>\n"
        f"• Hạn SLA: {deadline:%d/%m %H:%M}"
    )
    return Ticket(**row)
