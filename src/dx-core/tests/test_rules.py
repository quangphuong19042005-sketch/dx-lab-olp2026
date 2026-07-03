# SPDX-License-Identifier: MIT
"""Unit test cho rule engine + rào chắn Poka-yoke (thuần, không cần DB)."""
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from app import rules
from app.models import Category, Priority, TicketIn


def _ticket(**kw) -> TicketIn:
    base = dict(
        title="Máy lạnh không chạy",
        customer_name="Nguyễn Văn A",
        customer_phone="0901234567",
        category=Category.ky_thuat,
    )
    base.update(kw)
    return TicketIn(**base)


def test_infer_priority_ky_thuat_la_cao():
    assert rules.infer_priority(_ticket()) == Priority.cao


def test_infer_priority_ton_trong_gia_tri_cho_truoc():
    t = _ticket(category=Category.khac, priority=Priority.thap)
    assert rules.infer_priority(t) == Priority.thap


def test_assign_theo_loai():
    assert rules.assign(_ticket(category=Category.thanh_toan)) == "to-ke-toan"
    assert rules.assign(_ticket(category=Category.khac)) == "to-cskh"


def test_sla_uu_tien_cao_4_gio():
    now = datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc)
    deadline = rules.sla_deadline(Priority.cao, now)
    assert (deadline - now).total_seconds() == 4 * 3600


@pytest.mark.parametrize("phone", ["123", "090123", "abcxyz", ""])
def test_poka_yoke_chan_sdt_sai(phone):
    with pytest.raises(ValidationError):
        _ticket(customer_phone=phone)


@pytest.mark.parametrize("phone", ["0901234567", "+84901234567", "0356789123"])
def test_poka_yoke_cho_sdt_hop_le(phone):
    assert _ticket(customer_phone=phone).customer_phone == phone
