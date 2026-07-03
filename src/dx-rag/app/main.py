# SPDX-License-Identifier: MIT
"""DX-RAG API — trợ lý AI [I] bám tri thức nội bộ, chống ảo giác.

Luồng /ask: nhúng câu hỏi → tìm top-k đoạn liên quan trong Qdrant →
ghép ngữ cảnh → yêu cầu LLM CHỈ trả lời theo ngữ cảnh (không bịa).
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel, Field
from . import llm, store
from .config import settings
from .ingest import ingest

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("dx-rag")


async def _auto_ingest() -> None:
    """Tự nạp tri thức nếu kho trống — chạy nền, bỏ qua nếu LLM chưa sẵn sàng."""
    try:
        if await store.count() == 0:
            log.info("Kho tri thức trống — tự động nạp...")
            res = await ingest()
            log.info("Auto-ingest xong: %s", res)
        else:
            log.info("Kho tri thức đã có dữ liệu, bỏ qua auto-ingest.")
    except Exception as exc:  # không để lỗi nạp làm sập service
        log.warning("Auto-ingest thất bại (sẽ nạp lại qua POST /ingest): %s", exc)


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(_auto_ingest())
    yield


app = FastAPI(title="DX-RAG — Trợ lý AI nội bộ", version="0.4.0", lifespan=lifespan)

_PROMPT = """Bạn là trợ lý nội bộ của doanh nghiệp. CHỈ trả lời dựa trên NGỮ CẢNH dưới đây.
Nếu ngữ cảnh không chứa thông tin để trả lời, hãy nói đúng câu: "Xin lỗi, tôi không tìm thấy thông tin này trong tài liệu nội bộ." Tuyệt đối không bịa đặt.

NGỮ CẢNH:
{context}

CÂU HỎI: {question}
TRẢ LỜI (ngắn gọn, tiếng Việt):"""


class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class AskOut(BaseModel):
    answer: str
    sources: list[str]
    mode: str


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "dx-rag", "mode": settings.llm_mode}


@app.post("/ingest")
async def do_ingest() -> dict:
    return await ingest()


@app.post("/ask", response_model=AskOut)
async def ask(payload: AskIn) -> AskOut:
    try:
        qvec = await llm.embed(payload.question)
        hits = await store.search(qvec, limit=4)
    except Exception as exc:  # lỗi mạng/quota/kho chưa sẵn sàng → thông báo mềm
        log.warning("Lỗi truy vấn tri thức: %s", exc)
        return AskOut(
            answer="Trợ lý tạm thời bận (không truy vấn được tri thức). Vui lòng thử lại sau giây lát.",
            sources=[], mode=settings.llm_mode)

    if not hits:
        return AskOut(
            answer="Xin lỗi, kho tri thức chưa được nạp. Vui lòng chạy POST /ingest.",
            sources=[], mode=settings.llm_mode)

    context = "\n---\n".join(h["payload"]["text"] for h in hits)
    sources = sorted({h["payload"]["source"] for h in hits})
    try:
        answer = await llm.generate(_PROMPT.format(context=context, question=payload.question))
    except Exception as exc:
        log.warning("Lỗi sinh câu trả lời: %s", exc)
        return AskOut(
            answer="Trợ lý tạm thời bận (mô hình AI không phản hồi). Vui lòng thử lại.",
            sources=sources, mode=settings.llm_mode)
    return AskOut(answer=answer, sources=sources, mode=settings.llm_mode)
