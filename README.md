# End of Life (EoL) & Maintenance Deadline Management System

## **概要**

自社使用製品の End of Life (EoL) や定期的な保守期限を管理するシステムを開発する。

## **要件**

### **ユーザー管理**

- IdP として Okta を利用する。
- 認証機能は Okta に依存しない形とし、OpenID Connect（OIDC）および SAML をサポートする。
- ロール管理は実装しない。
- どのユーザーがどの製品を登録したかをログに記録する。

### **製品管理**

- 製品の登録、編集、削除、一覧表示。
- OS、ミドルウェア（DB、プログラミング言語、フレームワーク）、ネットワーク機器などの種別ごとに管理。
- 1つの製品が複数のカテゴリ（DEVELOPMENT、Operation など）に紐づけ可能。
- カテゴリの登録、編集、削除が可能。

### **EoL & 保守期限管理**

- 製品と EoL は 1:1 の関係。
- OS・ミドルウェアの EoL 情報を `https://endoflife.date/` から API で取得。
  - 取得先の例:
    - Oracle JDK: `https://endoflife.date/api/oracle-jdk.json`
    - CentOS: `https://endoflife.date/api/centos.json`
  - 更新頻度は 1 日 1 回。
  - 更新エラー時はエラーログを出力し、前回のデータを保持。
  - 更新のリトライは翌日の実行時に行う。
- 定期的な保守期限（例: サポート契約の期限）も管理対象とする。

### **ダッシュボード**

- 製品ごとの EoL 情報を一覧表示。
- カテゴリごとのフィルター機能（DEVELOPMENT、Operation）。

### **通知機能**

- EoL が近づいたら通知を送信。
- メール（SendGrid）と Slack 通知。
- 通知タイミングは 1 ヶ月前をデフォルトとし、カスタマイズ可能。
- 通知頻度: 1 ヶ月前、2 週間前、1 週間前、3 日前、1 日前。
- 通知履歴は DB ではなくログファイルに保存。

### **ログ機能**

- ユーザーの操作ログを記録（ユーザーID、操作内容、日時）。

### **CSV インポート / エクスポート**

- **エクスポート**: 製品・EoL 情報を CSV 形式で出力。
- **インポート**:
  - UTF-8 エンコード。
  - 製品情報（製品名、取引先会社（空欄可）、EoL 日）。
  - 日付フォーマットエラーはエラーとして表示。
  - 重複データは差分を比較し、ユーザーが選択可能。
  - CSV の差分比較 UI を提供（ハイライト付き）。

## **技術要件**

- **フロントエンド**: React, TypeScript, Material-UI
- **バックエンド**: FastAPI (Python)
- **データベース**: 初期は SQLite、運用では MySQL
- **非同期処理**: Celery + Redis（Job の WebUI は Flower）
- **スキーマ管理**: Atlas (`https://atlasgo.io/`)
- **キャッシュ**: Redis
- **CI/CD**: GitHub Actions
- **テスト**:
  - Jest, React Testing Library
  - MySQL のテストは Docker を利用
- **開発環境**:
  - Docker, Docker Compose
  - `docker-compose.yml` を `compose.yaml` に移行
  - MySQL も Docker で立ち上げ
- **Python パッケージ管理**: Poetry

## **データベース設計（HCL形式）**

```hcl
table "products" {
  schema = schema.public
  column "id" {
    null = false
    type = int
    auto_increment = true
  }
  column "name" {
    null = false
    type = varchar(255)
  }
  column "vendor" {
    null = true
    type = varchar(255)
  }
  column "category_id" {
    null = false
    type = int
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "fk_category" {
    columns     = [column.category_id]
    ref_columns = [table.categories.column.id]
  }
}

table "eol" {
  schema = schema.public
  column "id" {
    null = false
    type = int
    auto_increment = true
  }
  column "product_id" {
    null = false
    type = int
  }
  column "eol_date" {
    null = false
    type = date
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "fk_product" {
    columns     = [column.product_id]
    ref_columns = [table.products.column.id]
  }
}
```

## **API 設計（OpenAPI 準拠）**

```yaml
openapi: 3.0.0
info:
  title: Lifecycle Manager API
  version: 1.0.0
paths:
  /products:
    get:
      summary: 製品一覧を取得
      responses:
        '200':
          description: 成功
    post:
      summary: 製品を登録
      responses:
        '201':
          description: 製品登録成功
  /products/{id}:
    get:
      summary: 特定の製品情報を取得
      responses:
        '200':
          description: 成功
    put:
      summary: 製品情報を更新
      responses:
        '200':
          description: 更新成功
    delete:
      summary: 製品を削除
      responses:
        '204':
          description: 削除成功
  /eol:
    get:
      summary: EoL 情報を取得
      responses:
        '200':
          description: 成功
    post:
      summary: EoL を登録
      responses:
        '201':
          description: 登録成功
```

## **リポジトリ名**

- `lifecycle-manager` (採用)
- その他候補: `eol-tracker`, `maint-lifecycle`, `product-lifecycle`

## **今後のステップ**

1. バックエンド実装のディレクトリ構成を決定
2. FastAPI + Celery + Redis の環境構築
3. フロントエンドの基本 UI 作成
4. API 実装とテスト

