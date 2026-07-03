# SPDX-License-Identifier: MIT
"""Cấu hình DX-RAG — chọn backend LLM qua biến môi trường."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_mode: str = "api"  # "api" (Gemini) | "local" (Ollama)

    # Hướng API — Google Gemini
    gemini_api_key: str = ""
    gemini_chat_model: str = "gemini-2.5-flash"
    gemini_embed_model: str = "gemini-embedding-001"

    # Hướng cục bộ — Ollama
    ollama_host: str = "http://ollama:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_embed_model: str = "nomic-embed-text"

    # Vector DB
    qdrant_host: str = "http://qdrant:6333"
    collection: str = "dx_knowledge"


settings = Settings()
