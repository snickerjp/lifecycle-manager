import httpx
from datetime import datetime
from typing import List, Optional

from app.schemas.eol import EndoflifeApiResponse

class EndoflifeApiService:
    """endoflife.date APIとの連携を管理するサービス"""
    
    BASE_URL = "https://endoflife.date/api"

    @staticmethod
    async def get_product_info(product_name: str) -> List[EndoflifeApiResponse]:
        """
        指定された製品のEoL情報を取得します
        
        Args:
            product_name: 製品名（例: 'ubuntu', 'python'）
        Returns:
            List[EndoflifeApiResponse]: EoL情報のリスト
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{EndoflifeApiService.BASE_URL}/{product_name}.json")
            response.raise_for_status()
            
            # レスポンスをPydanticモデルに変換
            data = response.json()
            if isinstance(data, list):
                return [EndoflifeApiResponse(**item) for item in data]
            else:
                return [EndoflifeApiResponse(**data)]

    @staticmethod
    def parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """
        日付文字列をdatetimeオブジェクトに変換します
        
        Args:
            date_str: YYYY-MM-DD形式の日付文字列
        Returns:
            Optional[datetime]: 変換された日付、またはNone
        """
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None