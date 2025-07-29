# coding=utf-8
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.asset import Asset, AssetType, Exchange
from app.schemas.asset import (
    AssetResponse, AssetCreate, AssetUpdate,
    AssetTypeResponse, ExchangeResponse
    )

router = APIRouter()


@router.get("/", response_model=List[AssetResponse])
async def get_assets(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        asset_type: Optional[str] = None,
        exchange_code: Optional[str] = None,
        search: Optional[str] = None,
        db: Session = Depends(get_db)
        ):
    """자산 목록 조회 (필터링 지원)"""
    query = db.query(Asset).filter(Asset.is_active == True)

    # 자산 유형 필터
    if asset_type:
        query = query.join(AssetType).filter(AssetType.name == asset_type)

    # 거래소 필터
    if exchange_code:
        query = query.join(Exchange).filter(Exchange.code == exchange_code)

    # 검색 필터 (심볼 또는 이름)
    if search:
        query = query.filter(
            (Asset.symbol.ilike(f"%{search}%")) |
            (Asset.name.ilike(f"%{search}%"))
            )

    assets = query.offset(skip).limit(limit).all()
    return assets


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """특정 자산 상세 조회"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/", response_model=AssetResponse)
async def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """새 자산 등록"""
    # 중복 체크 (같은 거래소의 같은 심볼)
    existing = db.query(Asset).filter(
        Asset.symbol == asset.symbol,
        Asset.exchange_id == asset.exchange_id
        ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Asset with this symbol already exists in this exchange"
            )

    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(
        asset_id: int,
        asset_update: AssetUpdate,
        db: Session = Depends(get_db)
        ):
    """자산 정보 수정"""
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = asset_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)

    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """자산 삭제 (비활성화)"""
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    db_asset.is_active = False
    db.commit()
    return {"message": "Asset deleted successfully"}


@router.get("/types/", response_model=List[AssetTypeResponse])
async def get_asset_types(db: Session = Depends(get_db)):
    """자산 유형 목록 조회"""
    return db.query(AssetType).all()


@router.get("/exchanges/", response_model=List[ExchangeResponse])
async def get_exchanges(
        asset_type: Optional[str] = None,
        db: Session = Depends(get_db)
        ):
    """거래소 목록 조회"""
    query = db.query(Exchange).filter(Exchange.is_active == True)

    if asset_type:
        query = query.join(AssetType).filter(AssetType.name == asset_type)

    return query.all()