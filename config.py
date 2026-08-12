"""Конфигурация бота PotyjnoVPN."""
import os
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Config:
    """Конфигурация приложения."""

    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: List[int] = field(default_factory=list)
    ADMIN_CHAT_ID: int = int(os.getenv("ADMIN_CHAT_ID", "0"))

    # Channel
    CHANNEL_USERNAME: str = os.getenv("CHANNEL_USERNAME", "")

    # Remnawave
    REMNAWAVE_URL: str = os.getenv("REMNAWAVE_URL", "").rstrip("/")
    REMNAWAVE_TOKEN: str = os.getenv("REMNAWAVE_TOKEN", "")

    # Web
    WEB_HOST: str = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8080"))
    DOMAIN: str = os.getenv("DOMAIN", "").rstrip("/")

    # Traffic & Referral
    DEFAULT_TRAFFIC_GB: float = float(os.getenv("DEFAULT_TRAFFIC_GB", "50"))
    REFERRAL_BONUS_GB: float = float(os.getenv("REFERRAL_BONUS_GB", "1"))
    MAX_REFERRALS_PER_DAY: int = int(os.getenv("MAX_REFERRALS_PER_DAY", "25"))
    MAX_REFERRAL_BONUS_GB: float = float(os.getenv("MAX_REFERRAL_BONUS_GB", "25"))
    SUBSCRIPTION_DAYS: int = int(os.getenv("SUBSCRIPTION_DAYS", "30"))

    # Notifications
    NOTIFY_72H: bool = os.getenv("NOTIFY_72H", "true").lower() == "true"
    NOTIFY_10GB: bool = os.getenv("NOTIFY_10GB", "true").lower() == "true"
    NOTIFY_1GB: bool = os.getenv("NOTIFY_1GB", "true").lower() == "true"

    # Anti-fraud
    SUSPICIOUS_INTERVAL_SEC: int = 30
    SUSPICIOUS_ACCOUNT_AGE_DAYS: int = 7

    # DB
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "potyjn")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "potyjn_vpn")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def __post_init__(self):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        object.__setattr__(
            self,
            "ADMIN_IDS",
            [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()],
        )


config = Config()
