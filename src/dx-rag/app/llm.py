# SPDX-License-Identifier: MIT
"""Lớp trừu tượng LLM: nhúng (embed) + sinh văn bản (generate).
Hai backend: Gemini API (mặc định) hoặc Ollama cục bộ — chọn bằng LLM_MODE.
"""
import httpx
from .config import settings

_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models"


async def embed(text: str) -> list[float]:
    """Trả về véc-tơ nhúng của đoạn văn bản."""
    if settings.llm_mode == "local":
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{settings.ollama_host}/api/embeddings",
                             json={"model": settings.ollama_embed_model, "prompt": text})
            r.raise_for_status()
            return r.json()["embedding"]
    # Gemini
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(
            f"{_GEMINI}/{settings.gemini_embed_model}:embedContent",
            params={"key": settings.gemini_api_key},
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
        r = await c.post(
            f"{_GEMINI}/{settings.gemini_chat_model}:generateContent",
            params={"key": settings.gemini_api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
