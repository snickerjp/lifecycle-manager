from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    vendor: Optional[str] = None


class ProductCreate(ProductBase):
    category_ids: List[int]


class ProductUpdate(ProductBase):
    category_ids: List[int]


class Product(ProductBase):
    id: int
    categories: List[Category]
    created_by_user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True