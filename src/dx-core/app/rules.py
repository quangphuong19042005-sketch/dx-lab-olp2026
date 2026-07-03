# SPDX-License-Identifier: MIT
"""Rule engine — logic nghiệp vụ thuần, không phụ thuộc I/O (dễ unit test).

Đây là 'trục điều khiển' [P]: chuyển giao quyết định từ thao tác thủ công của
con người sang thuật toán (phân công + tính hạn SLA tự động).
"""
from datetime import datetime, timedelta
from .models import Category, Priority, TicketIn

# Bảng phân công theo loại yêu cầu (cấu hình đơn giản, sau nối DB/Keycloak group).
_ASSIGNEE_BY_CATEGORY: dict[Category, str] = {
    Category.ky_thuat: "to-ky-thuat",
    Category.thanh_toan: "to-ke-toan",
    Category.khac: "to-cskh",
}

# Hạn xử lý (giờ) theo mức ưu tiên.
_SLA_HOURS: dict[Priority, int] = {
    Priority.cao: 4,
    Priority.trung_binh: 24,
    Priority.thap: 72,
}


def infer_priority(ticket: TicketIn) -> Priority:
    """Nếu đầu vào chưa nêu ưu tiên: suy luận theo loại (kỹ thuật = cao)."""
    if ticket.priority is not None:
        return ticket.priority
    if ticket.category == Category.ky_thuat:
        return Priority.cao
    return Priority.trung_binh


def assign(ticket: TicketIn) -> str:
    """Chọn tổ/nhóm xử lý theo loại yêu cầu."""
    return _ASSIGNEE_BY_CATEGORY[ticket.category]


def sla_deadline(priority: Priority, now: datetime) -> datetime:
    """Tính mốc hạn chót dựa trên mức ưu tiên."""
    return now + timedelta(hours=_SLA_HOURS[priority])
