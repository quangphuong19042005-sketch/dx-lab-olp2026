# SPDX-License-Identifier: MIT
"""DX-RAG API — trợ lý AI [I] bám tri thức nội bộ, chống ảo giác.

Luồng /ask: nhúng câu hỏi → tìm top-k đoạn liên quan trong Qdrant →
ghép ngữ cảnh → yêu cầu LLM CHỈ trả lời theo ngữ cảnh (không bịa).
"""
import logging
from fastapi import FastAPI
from pydantic import BaseModel, Field
from . import llm, store
from .config import settings
from .ingest import ingest

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="DX-RAG — Trợ lý AI nội bộ", version="0.4.0")

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
    qvec = await llm.embed(payload.question)
    hits = await store.search(qvec, limit=4)
    if not hits:
        return AskOut(
            answer="Xin lỗi, kho tri thức chưa được nạp. Vui lòng chạy /ingest.",
            sources=[], mode=settings.llm_mode)

    context = "\n---\n".join(h["payload"]["text"] for h in hits)
    sources = sorted({h["payload"]["source"] for h in hits})
    answer = await llm.generate(_PROMPT.format(context=context, question=payload.question))
    return AskOut(answer=answer, sources=sources, mode=settings.llm_mode)
