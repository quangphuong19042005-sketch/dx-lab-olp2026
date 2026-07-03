# SPDX-License-Identifier: MIT
"""Cấu hình DX-Core — đọc từ biến môi trường (không hard-code bí mật)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # [D] PostgreSQL — nguồn sự thật duy nhất
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "dxlab"
    postgres_user: str = "dxlab"
    postgres_password: str = "dxlab"

    # [H] Telegram — kênh cảnh báo (tùy chọn; để trống thì chỉ ghi log)
    telegram_bot_token: str = ""
    telegram_alert_chat_id: str = ""

    @property
    def dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
