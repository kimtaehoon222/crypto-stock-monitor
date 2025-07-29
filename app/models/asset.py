# coding=utf-8
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class AssetType(Base):
    """자산 유형 (주식, 암호화폐 등)"""
    __tablename__ = "asset_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # 'stock', 'crypto'
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    assets = relationship("Asset", back_populates="asset_type")
    exchanges = relationship("Exchange", back_populates="asset_type")


class Exchange(Base):
    """거래소 정보"""
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    country = Column(String(50))
    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    api_endpoint = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    asset_type = relationship("AssetType", back_populates="exchanges")
    assets = relationship("Asset", back_populates="exchange")


class Asset(Base):
    """자산 정보 (개별 주식/코인)"""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)  # 'AAPL', 'BTC'
    name = Column(String(255), nullable=False)  # 'Apple Inc.', 'Bitcoin'
    exchange_id = Column(Integer, ForeignKey("exchanges.id"))
    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    description = Column(Text)
    market_cap = Column(BigInteger)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    exchange = relationship("Exchange", back_populates="assets")
    asset_type = relationship("AssetType", back_populates="assets")
    price_data = relationship("PriceData", back_populates="asset")
    user_watchlists = relationship("UserWatchlist", back_populates="asset")
    alert_settings = relationship("AlertSetting", back_populates="asset")


class PriceData(Base):
    """가격 데이터 (시계열)"""
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    price = Column(DECIMAL(20, 8), nullable=False)
    open_price = Column(DECIMAL(20, 8))
    high_price = Column(DECIMAL(20, 8))
    low_price = Column(DECIMAL(20, 8))
    close_price = Column(DECIMAL(20, 8))
    volume = Column(BigInteger)
    market_cap = Column(BigInteger)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    data_source = Column(String(50))  # API 소스 추적
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    asset = relationship("Asset", back_populates="price_data")

# 인덱스는 alembic 마이그레이션에서 생성 예정