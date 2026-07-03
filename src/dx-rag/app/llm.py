# SPDX-License-Identifier: MIT
"""Lớp trừu tượng LLM: nhúng (embed) + sinh văn bản (generate).
Hai backend: Gemini API (mặc định) hoặc Ollama cục bộ — chọn bằng LLM_MODE.
Khóa Gemini truyền qua header 'x-goog-api-key' (KHÔNG đưa vào URL để tránh lộ trong log).
"""
import asyncio
import httpx
from .config import settings

_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models"


def _gemini_headers() -> dict:
    return {"x-goog-api-key": settings.gemini_api_key}


async def _post_retry(client: httpx.AsyncClient, url: str, *, json: dict,
                      headers: dict | None = None, tries: int = 3) -> httpx.Response:
    """POST kèm retry cho lỗi 5xx tạm thời (Gemini hay 500/503 khi tải cao)."""
    last: Exception | None = None
    for i in range(tries):
        r = await client.post(url, json=json, headers=headers)
        if r.status_code < 500:
            return r
        last = httpx.HTTPStatusError(f"{r.status_code}", request=r.request, response=r)
        await asyncio.sleep(1.5 * (i + 1))
    if last:
        raise last
    return r


async def embed(text: str) -> list[float]:
    """Trả về véc-tơ nhúng của đoạn văn bản."""
    if settings.llm_mode == "local":
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{settings.ollama_host}/api/embeddings",
                             json={"model": settings.ollama_embed_model, "prompt": text})
            r.raise_for_status()
            return r.json()["embedding"]
    async with httpx.AsyncClient(timeout=60) as c:
        r = await _post_retry(
            c, f"{_GEMINI}/{settings.gemini_embed_model}:embedContent",
            headers=_gemini_headers(),
            json={"model": f"models/{settings.gemini_embed_model}",
                  "content": {"parts": [{"text": text}]}},
        )
        r.raise_for_status()
        return r.json()["embedding"]["values"]


async def generate(prompt: str) -> str:
    """Sinh câu trả lời từ prompt."""
    if settings.llm_mode == "local":
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post(f"{settings.ollama_host}/api/generate",
                             json={"model": settings.ollama_model, "prompt": prompt, "stream": False})
            r.raise_for_status()
            return r.json()["response"].strip()
    # Gemini
    async with httpx.AsyncClient(timeout=120) as c:
        r = await _post_retry(
            c, f"{_GEMINI}/{settings.gemini_chat_model}:generateContent",
            headers=_gemini_headers(),
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        r.raise_for_status()
        data = r.json()
        # Gemini có thể chặn nội dung (safety) → không có candidates.
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            return "Xin lỗi, tôi chưa tạo được câu trả lời cho câu hỏi này."
