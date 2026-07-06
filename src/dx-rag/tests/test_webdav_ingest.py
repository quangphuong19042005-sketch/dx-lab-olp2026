# SPDX-License-Identifier: MIT
"""Unit test cho parse WebDAV + chia đoạn tài liệu (thuần)."""
from app.webdav import parse_markdown_hrefs, is_configured
from app.ingest import _chunks

_PROPFIND = """<?xml version="1.0"?>
<d:multistatus xmlns:d="DAV:">
  <d:response><d:href>/remote.php/dav/files/admin/DX-Lab/3-Resources/</d:href></d:response>
  <d:response><d:href>/remote.php/dav/files/admin/DX-Lab/3-Resources/sop%20a.md</d:href></d:response>
  <d:response><d:href>/remote.php/dav/files/admin/DX-Lab/3-Resources/ghi-chu.txt</d:href></d:response>
  <d:response><d:href>/remote.php/dav/files/admin/DX-Lab/3-Resources/chinh-sach.md</d:href></d:response>
</d:multistatus>"""


def test_parse_chi_lay_md_va_giai_ma_url():
    hrefs = parse_markdown_hrefs(_PROPFIND)
    assert len(hrefs) == 2                       # bỏ thư mục & file .txt
    assert any(h.endswith("sop a.md") for h in hrefs)   # %20 → dấu cách
    assert all(h.lower().endswith(".md") for h in hrefs)


def test_is_configured_mac_dinh_false():
    # Chưa cấu hình Nextcloud → không dùng WebDAV.
    assert is_configured() is False


def test_chunks_loai_doan_ngan_va_giu_doan_dai():
    text = (
        "# Tiêu đề ngắn\n\n"
        "Đoạn nội dung thứ nhất đủ dài để vượt qua ngưỡng ba mươi ký tự bắt buộc.\n\n"
        "x\n\n"
        "Đoạn nội dung thứ hai cũng đủ dài để được giữ lại trong kết quả nhé."
    )
    chunks = _chunks(text)
    assert len(chunks) == 2
    assert all(len(c) >= 30 for c in chunks)
    assert "x" not in chunks
