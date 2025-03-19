from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.services.endoflife_api import EndoflifeApiService

router = APIRouter()

@router.get("/", response_model=List[schemas.EolInfo])
async def get_eol_info_list(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """EoL情報の一覧を取得します"""
    eol_info_list = db.query(models.EolInfo).offset(skip).limit(limit).all()
    return eol_info_list

@router.post("/", response_model=schemas.EolInfo)
async def create_eol_info(
    eol_info: schemas.EolInfoCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """新しいEoL情報を登録します"""
    # 製品の存在確認
    product = db.query(models.Product).filter(models.Product.id == eol_info.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された製品が見つかりません",
        )

    # EoL情報の作成
    db_eol_info = models.EolInfo(**eol_info.dict())
    db.add(db_eol_info)
    db.commit()
    db.refresh(db_eol_info)
    return db_eol_info

@router.get("/{eol_id}", response_model=schemas.EolInfo)
async def get_eol_info(
    eol_id: int,
    db: Session = Depends(deps.get_db),
):
    """指定されたEoL情報を取得します"""
    eol_info = db.query(models.EolInfo).filter(models.EolInfo.id == eol_id).first()
    if eol_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたEoL情報が見つかりません",
        )
    return eol_info

@router.put("/{eol_id}", response_model=schemas.EolInfo)
async def update_eol_info(
    eol_id: int,
    eol_info_update: schemas.EolInfoUpdate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """EoL情報を更新します"""
    eol_info = db.query(models.EolInfo).filter(models.EolInfo.id == eol_id).first()
    if eol_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたEoL情報が見つかりません",
        )

    # 更新可能なフィールドを更新
    for field, value in eol_info_update.dict().items():
        setattr(eol_info, field, value)
    
    db.add(eol_info)
    db.commit()
    db.refresh(eol_info)
    return eol_info

@router.delete("/{eol_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_eol_info(
    eol_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """EoL情報を削除します"""
    eol_info = db.query(models.EolInfo).filter(models.EolInfo.id == eol_id).first()
    if eol_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたEoL情報が見つかりません",
        )
    
    db.delete(eol_info)
    db.commit()
    return None

@router.post("/fetch/{product_name}", response_model=List[schemas.EolInfo])
async def fetch_eol_from_api(
    product_name: str,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    endoflife.date APIから指定された製品のEoL情報を取得し、
    データベースに保存します
    """
    try:
        # APIから情報取得
        api_response = await EndoflifeApiService.get_product_info(product_name)
        
        # 製品の存在確認
        product = db.query(models.Product).filter(
            models.Product.name.ilike(f"%{product_name}%")
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定された製品が見つかりません",
            )

        saved_eol_info = []
        for eol_data in api_response:
            if eol_data.eol and eol_data.releaseDate:
                # EoL情報の作成
                eol_info = models.EolInfo(
                    product_id=product.id,
                    eol_date=eol_data.releaseDate,
                    source="endoflife.date",
                    link=eol_data.link
                )
                db.add(eol_info)
                saved_eol_info.append(eol_info)

        db.commit()
        for info in saved_eol_info:
            db.refresh(info)
            
        return saved_eol_info

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"EoL情報の取得に失敗しました: {str(e)}",
        )