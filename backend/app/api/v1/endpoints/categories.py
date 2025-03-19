from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Category])
def get_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    カテゴリ一覧を取得します。
    """
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

@router.post("/", response_model=schemas.Category)
def create_category(
    category_in: schemas.CategoryCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    新しいカテゴリを作成します。
    """
    # 同名のカテゴリが存在するかチェック
    db_category = db.query(models.Category).filter(
        models.Category.name == category_in.name
    ).first()
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="指定された名前のカテゴリは既に存在します",
        )

    # カテゴリの作成
    db_category = models.Category(name=category_in.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/{category_id}", response_model=schemas.Category)
def get_category(
    category_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    カテゴリの詳細を取得します。
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたカテゴリが見つかりません",
        )
    return category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category_in: schemas.CategoryCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    カテゴリ情報を更新します。
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたカテゴリが見つかりません",
        )

    # 同名の別カテゴリが存在するかチェック
    existing_category = db.query(models.Category).filter(
        models.Category.name == category_in.name,
        models.Category.id != category_id
    ).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="指定された名前のカテゴリは既に存在します",
        )

    # カテゴリ情報の更新
    category.name = category_in.name
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    カテゴリを削除します。
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたカテゴリが見つかりません",
        )
    
    # カテゴリが製品に紐付けられているかチェック
    if category.products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このカテゴリは製品に使用されているため削除できません",
        )
    
    db.delete(category)
    db.commit()
    return None