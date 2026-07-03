# SPDX-License-Identifier: MIT
"""Tầng lưu trữ [D] — ghi ticket vào PostgreSQL (nguồn sự thật duy nhất)."""
from datetime import datetime
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from .config import settings

_DDL = """
CREATE TABLE IF NOT EXISTS tickets (
    id            SERIAL PRIMARY KEY,
    title         TEXT        NOT NULL,
    description   TEXT        NOT NULL DEFAULT '',
    customer_name TEXT        NOT NULL,
    customer_phone TEXT       NOT NULL,
    category      TEXT        NOT NULL,
    priority      TEXT        NOT NULL,
    assignee      TEXT        NOT NULL,
    status        TEXT        NOT NULL DEFAULT 'moi',
    sla_deadline  TIMESTAMPTZ NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

pool = AsyncConnectionPool(settings.dsn, open=False, min_size=1, max_size=5)


async def init_schema() -> None:
    """Tạo bảng tickets nếu chưa có (idempotent)."""
    async with pool.connection() as conn:
        await conn.execute(_DDL)


async def insert_ticket(
    data: dict, assignee: str, priority: str, deadline: datetime
) -> dict:
    """Chèn ticket đã chuẩn hóa, trả về bản ghi đầy đủ."""
    async with pool.connection() as conn:
        conn.row_factory = dict_row
        cur = await conn.execute(
            """
            INSERT INTO tickets
                (title, description, customer_name, customer_phone,
                 category, priority, assignee, sla_deadline)
            VALUES (%(title)s, %(description)s, %(customer_name)s, %(customer_phone)s,
                    %(category)s, %(priority)s, %(assignee)s, %(sla_deadline)s)
            RETURNING *;
            """,
            {
                "title": data["title"],
                "description": data["description"],
                "customer_name": data["customer_name"],
                "customer_phone": data["customer_phone"],
                "category": data["category"],
                "priority": priority,
                "assignee": assignee,
                "sla_deadline": deadline,
            },
        )
        return await cur.fetchone()
