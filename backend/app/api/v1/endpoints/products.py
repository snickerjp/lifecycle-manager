from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def get_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    製品一覧を取得します。
    """
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@router.post("/", response_model=schemas.Product)
def create_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    新しい製品を作成します。
    """
    # カテゴリの存在確認
    categories = db.query(models.Category).filter(
        models.Category.id.in_(product_in.category_ids)
    ).all()
    if len(categories) != len(product_in.category_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="指定されたカテゴリの一部が存在しません",
        )

    # 製品の作成
    db_product = models.Product(
        name=product_in.name,
        vendor=product_in.vendor,
        created_by_user_id=current_user_id,
        categories=categories
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    製品の詳細を取得します。
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された製品が見つかりません",
        )
    return product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_in: schemas.ProductUpdate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    製品情報を更新します。
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された製品が見つかりません",
        )

    # カテゴリの存在確認
    categories = db.query(models.Category).filter(
        models.Category.id.in_(product_in.category_ids)
    ).all()
    if len(categories) != len(product_in.category_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="指定されたカテゴリの一部が存在しません",
        )

    # 製品情報の更新
    product.name = product_in.name
    product.vendor = product_in.vendor
    product.categories = categories
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id),
):
    """
    製品を削除します。
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された製品が見つかりません",
        )
    
    db.delete(product)
    db.commit()
    return None