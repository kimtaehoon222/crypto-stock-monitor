# coding=utf-8
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


# ===== AssetType 스키마 =====
class AssetTypeBase(BaseModel):
    name: str = Field(..., description="자산 유형 이름", example="crypto")
    description: Optional[str] = Field(None, description="자산 유형 설명", example="암호화폐")


class AssetTypeCreate(AssetTypeBase):
    pass


class AssetTypeResponse(AssetTypeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Exchange 스키마 =====
class ExchangeBase(BaseModel):
    name: str = Field(..., description="거래소 이름", example="Binance")
    code: str = Field(..., description="거래소 코드", example="BINANCE")
    country: Optional[str] = Field(None, description="국가", example="Global")
    api_endpoint: Optional[str] = Field(None, description="API 엔드포인트")


class ExchangeCreate(ExchangeBase):
    asset_type_id: int = Field(..., description="자산 유형 ID")


class ExchangeResponse(ExchangeBase):
    id: int
    asset_type_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Asset 스키마 =====
class AssetBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="심볼", example="BTC")
    name: str = Field(..., min_length=1, max_length=255, description="자산 이름", example="Bitcoin")
    description: Optional[str] = Field(None, description="자산 설명")

    @validator('symbol')
    def symbol_must_be_uppercase(cls, v):
        return v.upper().strip()

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('자산 이름은 비어있을 수 없습니다')
        return v.strip()


class AssetCreate(AssetBase):
    exchange_id: int = Field(..., description="거래소 ID")
    asset_type_id: int = Field(..., description="자산 유형 ID")
    market_cap: Optional[int] = Field(None, ge=0, description="시가총액")


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="자산 이름")
    description: Optional[str] = Field(None, description="자산 설명")
    market_cap: Optional[int] = Field(None, ge=0, description="시가총액")
    is_active: Optional[bool] = Field(None, description="활성 상태")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('자산 이름은 비어있을 수 없습니다')
        return v.strip() if v else v


class AssetResponse(AssetBase):
    id: int
    exchange_id: int
    asset_type_id: int
    market_cap: Optional[int]
    is_active: bool
    created_at: datetime

    # 관계 데이터 포함 (선택적)
    exchange: Optional[ExchangeResponse] = None
    asset_type: Optional[AssetTypeResponse] = None

    class Config:
        from_attributes = True


# ===== 가격 데이터 스키마 =====
class PriceDataBase(BaseModel):
    price: Decimal = Field(..., gt=0, description="현재 가격")
    open_price: Optional[Decimal] = Field(None, ge=0, description="시가")
    high_price: Optional[Decimal] = Field(None, ge=0, description="고가")
    low_price: Optional[Decimal] = Field(None, ge=0, description="저가")
    close_price: Optional[Decimal] = Field(None, ge=0, description="종가")
    volume: Optional[int] = Field(None, ge=0, description="거래량")
    market_cap: Optional[int] = Field(None, ge=0, description="시가총액")
    timestamp: datetime = Field(..., description="데이터 시간")
    data_source: Optional[str] = Field(None, description="데이터 소스", example="coingecko")

    @validator('high_price')
    def high_must_be_gte_low(cls, v, values):
        if v is not None and 'low_price' in values and values['low_price'] is not None:
            if v < values['low_price']:
                raise ValueError('고가는 저가보다 높아야 합니다')
        return v


class PriceDataCreate(PriceDataBase):
    asset_id: int = Field(..., description="자산 ID")


class PriceDataResponse(PriceDataBase):
    id: int
    asset_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ===== 자산 상세 정보 (가격 포함) =====
class AssetWithLatestPrice(AssetResponse):
    """최신 가격 정보가 포함된 자산 정보"""
    latest_price: Optional[PriceDataResponse] = None
    price_change_24h: Optional[Decimal] = Field(None, description="24시간 가격 변동")
    price_change_percent_24h: Optional[float] = Field(None, description="24시간 가격 변동률 (%)")


# ===== 자산 통계 스키마 =====
class AssetStats(BaseModel):
    """자산 통계 정보"""
    asset_id: int
    symbol: str
    name: str
    current_price: Optional[Decimal]
    price_24h_ago: Optional[Decimal]
    price_change_24h: Optional[Decimal]
    price_change_percent_24h: Optional[float]
    volume_24h: Optional[int]
    market_cap: Optional[int]
    high_24h: Optional[Decimal]
    low_24h: Optional[Decimal]
    last_updated: Optional[datetime]


# ===== 자산 목록 응답 (페이지네이션) =====
class AssetListResponse(BaseModel):
    """자산 목록 응답 (페이지네이션 정보 포함)"""
    items: list[AssetResponse]
    total: int
    page: int
    size: int
    pages: int