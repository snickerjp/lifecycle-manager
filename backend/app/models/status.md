status.md

これまでに実装した機能を整理します：

1. 環境構築
Docker環境の整備

FastAPIアプリケーション用のDockerfile
Redis用のコンテナ設定
MySQL用のコンテナ設定
Docker Compose による環境構築
Poetry による Python 環境管理

pyproject.toml での依存関係管理
開発環境とプロダクション環境の分離
2. FastAPIの基本セットアップ
アプリケーション構造の整備
backend/
├── app/
│   ├── main.py              # メインアプリケーション
│   ├── api/                 # APIルーター
│   │   ├── deps.py         # 依存関係（DB接続など）
│   │   └── v1/            # APIバージョン1
│   │       ├── api.py     # メインルーター
│   │       └── endpoints/  # エンドポイント実装
│   ├── models/             # SQLAlchemyモデル
│   └── schemas/            # Pydanticスキーマ

3. 実装済みのエンドポイント
製品管理 (/api/v1/products)

GET /products - 製品一覧取得
POST /products - 製品登録
GET /products/{id} - 製品詳細取得
PUT /products/{id} - 製品更新
DELETE /products/{id} - 製品削除
カテゴリ管理 (/api/v1/categories)

GET /categories - カテゴリ一覧取得
POST /categories - カテゴリ登録
GET /categories/{id} - カテゴリ詳細取得
PUT /categories/{id} - カテゴリ更新
DELETE /categories/{id} - カテゴリ削除

4. データモデル実装
製品モデル

基本情報（名前、ベンダー）
カテゴリとの多対多関連
タイムスタンプ（作成日時、更新日時）
カテゴリモデル

基本情報（名前）
製品との多対多関連


次に実装可能な機能
データベース接続の本格実装

SQLAlchemy セッション管理
マイグレーション（Alembic）
EoL管理機能

EoL情報の CRUD
endoflife.date APIとの連携
認証システム

Okta統合
JWTによる認証