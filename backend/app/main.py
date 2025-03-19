from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import router as api_v1_router

app = FastAPI(
    title="Lifecycle Manager",
    description="EoL & Maintenance Deadline Management System",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Lifecycle Manager API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# v1 APIルーターの統合
app.include_router(api_v1_router, prefix="/api/v1")