from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class MaintenanceBase(BaseModel):
    """保守期限の基本スキーマ"""
    product_id: int
    maintenance_deadline: date
    notes: Optional[str] = None  # 保守に関する備考
    contract_info: Optional[str] = None  # 契約情報

class MaintenanceCreate(MaintenanceBase):
    """保守期限作成用スキーマ"""
    pass

class MaintenanceUpdate(MaintenanceBase):
    """保守期限更新用スキーマ"""
    pass

class Maintenance(MaintenanceBase):
    """保守期限レスポース用スキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True