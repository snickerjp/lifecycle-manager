from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Maintenance])
async def get_maintenance_list(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """保守期限情報の一覧を取得します"""
    maintenance_list = db.query(models.Maintenance).offset(skip).limit(limit).all()
    return maintenance_list

@router.post("/", response_model=schemas.Maintenance)
async def create_maintenance(
    maintenance: schemas.MaintenanceCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """新しい保守期限情報を登録します"""
    # 製品の存在確認
    product = db.query(models.Product).filter(models.Product.id == maintenance.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された製品が見つかりません",
        )

    # 保守期限情報の作成
    db_maintenance = models.Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.get("/{maintenance_id}", response_model=schemas.Maintenance)
async def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(deps.get_db),
):
    """指定された保守期限情報を取得します"""
    maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された保守期限情報が見つかりません",
        )
    return maintenance

@router.put("/{maintenance_id}", response_model=schemas.Maintenance)
async def update_maintenance(
    maintenance_id: int,
    maintenance_update: schemas.MaintenanceUpdate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """保守期限情報を更新します"""
    maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された保守期限情報が見つかりません",
        )

    # 製品の存在確認
    if maintenance_update.product_id != maintenance.product_id:
        product = db.query(models.Product).filter(models.Product.id == maintenance_update.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された製品が見つかりません",
            )

    # 更新可能なフィールドを更新
    for field, value in maintenance_update.dict().items():
        setattr(maintenance, field, value)
    
    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)
    return maintenance

@router.delete("/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """保守期限情報を削除します"""
    maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if maintenance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された保守期限情報が見つかりません",
        )
    
    db.delete(maintenance)
    db.commit()
    return None