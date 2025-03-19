from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class EolInfoBase(BaseModel):
    """EoL情報の基本スキーマ"""
    product_id: int
    eol_date: date
    source: Optional[str] = None  # 情報ソース（例：endoflife.date, manual）
    link: Optional[str] = None    # 詳細情報へのリンク

class EolInfoCreate(EolInfoBase):
    """EoL情報作成用スキーマ"""
    pass

class EolInfoUpdate(EolInfoBase):
    """EoL情報更新用スキーマ"""
    pass

class EolInfo(EolInfoBase):
    """EoL情報レスポース用スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class EndoflifeApiResponse(BaseModel):
    """endoflife.date APIのレスポンススキーマ"""
    cycle: str
    releaseDate: Optional[str]
    eol: Optional[bool]
    latest: Optional[str]
    latestReleaseDate: Optional[str]
    link: Optional[str]