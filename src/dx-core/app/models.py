# SPDX-License-Identifier: MIT
"""Mô hình dữ liệu ticket + rào chắn Poka-yoke (xác thực đầu vào)."""
import re
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator

# Rào chắn định dạng SĐT Việt Nam (Poka-yoke ngay tại đầu nguồn — chống rác đầu vào).
_PHONE_RE = re.compile(r"^(0\d{9}|\+84\d{9})$")


class Category(str, Enum):
    ky_thuat = "ky_thuat"      # Kỹ thuật
    thanh_toan = "thanh_toan"  # Thanh toán
    khac = "khac"              # Khác


class Priority(str, Enum):
    cao = "cao"
    trung_binh = "trung_binh"
    thap = "thap"


class TicketIn(BaseModel):
    """Payload thô nhận từ biểu mẫu Baserow / DX-Portal."""
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(default="", max_length=2000)
    customer_name: str = Field(min_length=1, max_length=100)
    customer_phone: str
    category: Category = Category.khac
    priority: Priority | None = None

    @field_validator("customer_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip().replace(" ", "")
        if not _PHONE_RE.match(v):
            raise ValueError("Số điện thoại không hợp lệ (VD: 0901234567 hoặc +84901234567)")
        return v


class Ticket(TicketIn):
    """Ticket đã chuẩn hóa + gắn quyết định của rule engine."""
    id: int
    assignee: str
    sla_deadline: datetime
    status: str = "moi"
    created_at: datetime
