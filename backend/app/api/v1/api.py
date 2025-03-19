from fastapi import APIRouter
from app.api.v1.endpoints import products, categories, eol, maintenance

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

# 製品管理エンドポイントの統合
router.include_router(products.router, prefix="/products", tags=["products"])

# カテゴリ管理エンドポイントの統合
router.include_router(categories.router, prefix="/categories", tags=["categories"])

# EoL管理エンドポイントの統合
router.include_router(eol.router, prefix="/eol", tags=["eol"])

# 保守期限管理エンドポイントの統合
router.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])