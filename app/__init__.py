# coding=utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.models import user, asset, price, alert
from app.api.endpoints import assets, prices, users, alerts
from app.services.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 이벤트"""
    # 시작 시
    print("🚀 애플리케이션 시작")

    # 데이터베이스 테이블 생성
    user.Base.metadata.create_all(bind=engine)
    asset.Base.metadata.create_all(bind=engine)
    price.Base.metadata.create_all(bind=engine)
    alert.Base.metadata.create_all(bind=engine)

    # 스케줄러 시작
    start_scheduler()

    yield

    # 종료 시
    print("⏹️ 애플리케이션 종료")
    stop_scheduler()


app = FastAPI(
    title="Crypto Stock Monitor API",
    description="주식/암호화폐 가격 모니터링 시스템",
    version="1.0.0",
    lifespan=lifespan
    )

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 운영시에는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

# API 라우터 등록
app.include_router(
    assets.router,
    prefix="/api/v1/assets",
    tags=["assets"]
    )

app.include_router(
    prices.router,
    prefix="/api/v1/prices",
    tags=["prices"]
    )

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"]
    )

app.include_router(
    alerts.router,
    prefix="/api/v1/alerts",
    tags=["alerts"]
    )


@app.get("/")
async def root():
    return {
        "message": "Crypto Stock Monitor API",
        "version": "1.0.0",
        "docs": "/docs"
        }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)