# coding=utf-8
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 앱 기본 설정
    APP_NAME: str = "Crypto Stock Monitor"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://postgres:admin123@localhost:5432/crypto_monitor"

    # JWT 설정
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 외부 API 키들
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None
    BINANCE_API_KEY: Optional[str] = None
    BINANCE_SECRET_KEY: Optional[str] = None

    # Redis 설정 (캐싱용)
    REDIS_URL: str = "redis://localhost:6379/0"

    # 스케줄러 설정
    PRICE_UPDATE_INTERVAL: int = 60  # 초 단위 (1분마다)
    ALERT_CHECK_INTERVAL: int = 30  # 알림 체크 간격

    # 이메일 설정 (알림용)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # 로깅 설정
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()