from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    データベースセッションの依存関係
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id() -> int:
    """
    現在のユーザーIDを取得します（認証実装後に更新予定）
    """
    # TODO: JWT認証の実装後、トークンからユーザーIDを取得するように更新
    return 1  # 開発用の仮のユーザーID