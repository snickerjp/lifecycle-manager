from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class EolInfo(Base):
    __tablename__ = "eol_info"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    eol_date = Column(Date, nullable=False)
    source = Column(String, nullable=True)  # 情報ソース（例：endoflife.date, manual）
    link = Column(String, nullable=True)    # 詳細情報へのリンク
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # リレーションシップ
    product = relationship("Product", back_populates="eol_info")