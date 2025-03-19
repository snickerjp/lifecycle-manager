バックエンドのAPI設計を進めます。  
まず、エンドポイントの一覧を整理し、それぞれのリクエスト・レスポンス仕様を決めていきます。

---

## **APIエンドポイント一覧**

### **1. 認証関連**
| メソッド | エンドポイント         | 説明                      |
|----------|--------------------|--------------------------|
| GET      | `/auth/login`       | ログイン（Okta OIDC/SAML連携） |
| POST     | `/auth/logout`      | ログアウト               |
| GET      | `/auth/me`          | ログインユーザー情報取得 |

---

### **2. 製品管理**
| メソッド | エンドポイント          | 説明                       |
|----------|---------------------|---------------------------|
| GET      | `/products`          | 製品一覧取得                |
| POST     | `/products`          | 製品登録                    |
| GET      | `/products/{id}`     | 製品詳細取得                |
| PUT      | `/products/{id}`     | 製品更新                    |
| DELETE   | `/products/{id}`     | 製品削除                    |

#### **リクエスト例**
```json
{
  "name": "Ubuntu 22.04",
  "vendor": "Canonical",
  "category_ids": [1, 2]
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "name": "Ubuntu 22.04",
  "vendor": "Canonical",
  "categories": ["DEVELOPMENT", "Operation"]
}
```

---

### **3. カテゴリ管理**
| メソッド | エンドポイント          | 説明                       |
|----------|---------------------|---------------------------|
| GET      | `/categories`       | カテゴリ一覧取得            |
| POST     | `/categories`       | カテゴリ登録                |
| PUT      | `/categories/{id}`  | カテゴリ更新                |
| DELETE   | `/categories/{id}`  | カテゴリ削除                |

#### **リクエスト例**
```json
{
  "name": "DEVELOPMENT"
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "name": "DEVELOPMENT"
}
```

---

### **4. EoL管理**
| メソッド | エンドポイント           | 説明                       |
|----------|----------------------|---------------------------|
| GET      | `/eol`               | EoL情報一覧取得             |
| POST     | `/eol`               | EoL情報登録                 |
| GET      | `/eol/{id}`          | EoL情報詳細取得             |
| PUT      | `/eol/{id}`          | EoL情報更新                 |
| DELETE   | `/eol/{id}`          | EoL情報削除                 |
| POST     | `/eol/fetch`         | `endoflife.date` からデータ取得 |

#### **リクエスト例**
```json
{
  "product_id": 1,
  "eol_date": "2025-04-30"
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "product_id": 1,
  "product_name": "Ubuntu 22.04",
  "eol_date": "2025-04-30"
}
```

---

### **5. 保守期限管理**
| メソッド | エンドポイント                 | 説明                       |
|----------|-------------------------|---------------------------|
| GET      | `/maintenance`           | 保守期限一覧取得              |
| POST     | `/maintenance`           | 保守期限登録                  |
| GET      | `/maintenance/{id}`      | 保守期限詳細取得              |
| PUT      | `/maintenance/{id}`      | 保守期限更新                  |
| DELETE   | `/maintenance/{id}`      | 保守期限削除                  |

#### **リクエスト例**
```json
{
  "product_id": 1,
  "maintenance_deadline": "2024-12-01"
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "product_id": 1,
  "product_name": "Ubuntu 22.04",
  "maintenance_deadline": "2024-12-01"
}
```

---

### **6. 通知管理**
| メソッド | エンドポイント               | 説明                        |
|----------|-----------------------|--------------------------|
| GET      | `/notifications`       | 通知履歴一覧取得              |
| POST     | `/notifications/test`  | 通知テスト送信                |

#### **レスポンス例**
```json
{
  "id": 1,
  "type": "EoL",
  "product_name": "Ubuntu 22.04",
  "notification_date": "2024-11-01"
}
```

---

### **7. CSVインポート・エクスポート**
| メソッド | エンドポイント             | 説明                        |
|----------|---------------------|--------------------------|
| POST     | `/import`           | CSVデータインポート        |
| GET      | `/export`           | CSVデータエクスポート        |

---

### **8. ログ管理**
| メソッド | エンドポイント               | 説明                       |
|----------|-----------------------|---------------------------|
| GET      | `/logs`               | ログ一覧取得                 |

#### **レスポンス例**
```json
[
  {
    "id": 1,
    "user": "admin",
    "action": "製品登録",
    "timestamp": "2024-02-18T10:00:00"
  }
]
```

---

## **次のステップ**
- 各エンドポイントの詳細な仕様（リクエスト・レスポンスの型定義）
- APIの認可（どのエンドポイントを誰が実行できるか）
- バックエンド実装のディレクトリ構成

このAPI設計で問題なさそうでしょうか？バックエンドのAPI設計を進めます。  
まず、エンドポイントの一覧を整理し、それぞれのリクエスト・レスポンス仕様を決めていきます。

---

## **APIエンドポイント一覧**

### **1. 認証関連**
| メソッド | エンドポイント         | 説明                      |
|----------|--------------------|--------------------------|
| GET      | `/auth/login`       | ログイン（Okta OIDC/SAML連携） |
| POST     | `/auth/logout`      | ログアウト               |
| GET      | `/auth/me`          | ログインユーザー情報取得 |

---

### **2. 製品管理**
| メソッド | エンドポイント          | 説明                       |
|----------|---------------------|---------------------------|
| GET      | `/products`          | 製品一覧取得                |
| POST     | `/products`          | 製品登録                    |
| GET      | `/products/{id}`     | 製品詳細取得                |
| PUT      | `/products/{id}`     | 製品更新                    |
| DELETE   | `/products/{id}`     | 製品削除                    |

#### **リクエスト例**
```json
{
  "name": "Ubuntu 22.04",
  "vendor": "Canonical",
  "category_ids": [1, 2]
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "name": "Ubuntu 22.04",
  "vendor": "Canonical",
  "categories": ["DEVELOPMENT", "Operation"]
}
```

---

### **3. カテゴリ管理**
| メソッド | エンドポイント          | 説明                       |
|----------|---------------------|---------------------------|
| GET      | `/categories`       | カテゴリ一覧取得            |
| POST     | `/categories`       | カテゴリ登録                |
| PUT      | `/categories/{id}`  | カテゴリ更新                |
| DELETE   | `/categories/{id}`  | カテゴリ削除                |

#### **リクエスト例**
```json
{
  "name": "DEVELOPMENT"
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "name": "DEVELOPMENT"
}
```

---

### **4. EoL管理**
| メソッド | エンドポイント           | 説明                       |
|----------|----------------------|---------------------------|
| GET      | `/eol`               | EoL情報一覧取得             |
| POST     | `/eol`               | EoL情報登録                 |
| GET      | `/eol/{id}`          | EoL情報詳細取得             |
| PUT      | `/eol/{id}`          | EoL情報更新                 |
| DELETE   | `/eol/{id}`          | EoL情報削除                 |
| POST     | `/eol/fetch`         | `endoflife.date` からデータ取得 |

#### **リクエスト例**
```json
{
  "product_id": 1,
  "eol_date": "2025-04-30"
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "product_id": 1,
  "product_name": "Ubuntu 22.04",
  "eol_date": "2025-04-30"
}
```

---

### **5. 保守期限管理**
| メソッド | エンドポイント                 | 説明                       |
|----------|-------------------------|---------------------------|
| GET      | `/maintenance`           | 保守期限一覧取得              |
| POST     | `/maintenance`           | 保守期限登録                  |
| GET      | `/maintenance/{id}`      | 保守期限詳細取得              |
| PUT      | `/maintenance/{id}`      | 保守期限更新                  |
| DELETE   | `/maintenance/{id}`      | 保守期限削除                  |

#### **リクエスト例**
```json
{
  "product_id": 1,
  "maintenance_deadline": "2024-12-01"
}
```

#### **レスポンス例**
```json
{
  "id": 1,
  "product_id": 1,
  "product_name": "Ubuntu 22.04",
  "maintenance_deadline": "2024-12-01"
}
```

---

### **6. 通知管理**
| メソッド | エンドポイント               | 説明                        |
|----------|-----------------------|--------------------------|
| GET      | `/notifications`       | 通知履歴一覧取得              |
| POST     | `/notifications/test`  | 通知テスト送信                |

#### **レスポンス例**
```json
{
  "id": 1,
  "type": "EoL",
  "product_name": "Ubuntu 22.04",
  "notification_date": "2024-11-01"
}
```

---

### **7. CSVインポート・エクスポート**
| メソッド | エンドポイント             | 説明                        |
|----------|---------------------|--------------------------|
| POST     | `/import`           | CSVデータインポート        |
| GET      | `/export`           | CSVデータエクスポート        |

---

### **8. ログ管理**
| メソッド | エンドポイント               | 説明                       |
|----------|-----------------------|---------------------------|
| GET      | `/logs`               | ログ一覧取得                 |

#### **レスポンス例**
```json
[
  {
    "id": 1,
    "user": "admin",
    "action": "製品登録",
    "timestamp": "2024-02-18T10:00:00"
  }
]
```

---

## **次のステップ**
- 各エンドポイントの詳細な仕様（リクエスト・レスポンスの型定義）
- APIの認可（どのエンドポイントを誰が実行できるか）
- バックエンド実装のディレクトリ構成

このAPI設計で問題なさそうでしょうか？

---

FastAPI で **ログイン済みのユーザーのみが更新可能** にするには、以下の方法を組み合わせると実現できます。

### **1. 認証の仕組み**
Okta の OIDC (OpenID Connect) や SAML を使用するので、**アクセストークン (JWT) を用いた認証** が適切です。  
FastAPI の **`fastapi-users`** ライブラリを使うと、OIDC との統合がしやすくなります。

### **2. 認可の基本ルール**
- **全ユーザーがアクセスできるエンドポイント**
  - ログイン (`/auth/login`)
  - ログアウト (`/auth/logout`)
  - 製品一覧取得 (`GET /products`)
  - EoL情報取得 (`GET /eol`)

- **ログインユーザーのみ実行できるエンドポイント**
  - 製品の登録・更新・削除 (`POST /products`, `PUT /products/{id}`, `DELETE /products/{id}`)
  - EoL情報の登録・更新・削除 (`POST /eol`, `PUT /eol/{id}`, `DELETE /eol/{id}`)
  - CSV インポート (`POST /csv/import`)
  - 通知設定の変更 (`PUT /notifications/settings`)

### **3. 認証ミドルウェアの実装**
FastAPI の `Depends` を使って、JWT の検証を行い、ログイン済みユーザーのみが操作できるようにします。

#### **(1) 必要なライブラリをインストール**
```sh
pip install fastapi-users[sqlalchemy] authlib
```

#### **(2) 認証用の設定**
```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth

# Okta の OIDC 設定
OKTA_DOMAIN = "your-okta-domain"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

oauth = OAuth()
oauth.register(
    name="okta",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"https://{OKTA_DOMAIN}/oauth2/default/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# JWT 検証の設定
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize",
    tokenUrl=f"https://{OKTA_DOMAIN}/oauth2/default/v1/token"
)

async def get_current_user(token: str = Security(oauth2_scheme)):
    """JWT トークンを検証し、ユーザー情報を取得する"""
    try:
        user_info = await oauth.okta.parse_id_token(token)
        return user_info
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
```

#### **(3) エンドポイントに認証を適用**
```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.post("/products")
async def create_product(product_data: dict, user: dict = Depends(get_current_user)):
    """ログインユーザーのみが製品を登録できる"""
    return {"message": "Product created", "user": user["email"]}
```

---

## **まとめ**
- Okta の OIDC を使用し、OAuth2 のトークン検証 (`oauth2_scheme`) を行う
- `Depends(get_current_user)` を使って **認証必須エンドポイントを保護**
- ユーザーがログインしていない場合、`401 Unauthorized` を返す

この方法なら、**認可のルールをシンプルにしつつ、拡張もしやすい** ので、実装しながら微調整が可能です。  
他にも管理者権限を追加するなら、JWT の **`role` クレーム** を見て制御するのもアリですね。

---

はい、FastAPI は **OpenAPI** に準拠した API ドキュメントを自動生成できます。  
**APIの仕様を OpenAPI 形式（YAML または JSON）で記述することも可能** ですし、FastAPI のエンドポイント定義から OpenAPI スキーマを自動生成することもできます。

---

## **OpenAPI 仕様の記述方法**
### **1. FastAPI で自動生成**
FastAPI でエンドポイントを定義すると、自動的に OpenAPI ドキュメントが生成され、`/docs`（Swagger UI）や `/redoc`（ReDoc）で確認できます。

#### **APIエンドポイント例**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

# リクエスト/レスポンスのスキーマ
class Product(BaseModel):
    id: int
    name: str
    vendor: str | None
    eol_date: datetime.date

# 製品一覧取得 API
@app.get("/products", response_model=List[Product])
async def get_products():
    return [
        {"id": 1, "name": "Oracle JDK", "vendor": "Oracle", "eol_date": "2026-09-30"},
        {"id": 2, "name": "CentOS 7", "vendor": "Red Hat", "eol_date": "2024-06-30"}
    ]

# 製品登録 API
@app.post("/products", response_model=Product)
async def create_product(product: Product):
    return product
```

---

### **2. OpenAPI の JSON/YAML を確認**
FastAPI は自動的に **`/openapi.json`** で OpenAPI 仕様を出力します。

#### **確認方法**
- `http://127.0.0.1:8000/openapi.json` にアクセスすると、JSON 形式の OpenAPI ドキュメントを取得できます。
- `http://127.0.0.1:8000/docs` で Swagger UI から API を確認できます。
- `http://127.0.0.1:8000/redoc` で ReDoc から API を確認できます。

---

### **3. OpenAPI 仕様（YAML 形式）**
手動で OpenAPI 仕様を記述する場合、以下のように YAML 形式で定義できます。

```yaml
openapi: 3.0.0
info:
  title: End of Life Management API
  version: 1.0.0
paths:
  /products:
    get:
      summary: 製品一覧を取得
      operationId: getProducts
      responses:
        "200":
          description: 製品リストを返す
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Product"
    post:
      summary: 製品を登録
      operationId: createProduct
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Product"
      responses:
        "201":
          description: 登録された製品を返す
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Product"

components:
  schemas:
    Product:
      type: object
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "Oracle JDK"
        vendor:
          type: string
          example: "Oracle"
        eol_date:
          type: string
          format: date
          example: "2026-09-30"
```

この YAML を **Swagger Editor（https://editor.swagger.io/）** に貼り付けると、API の仕様を視覚的に確認できます。

---

## **次のステップ**
- **FastAPI の API 実装を進めながら、自動生成された OpenAPI を確認する**
- **YAML 形式の OpenAPI 定義を作成し、必要なら手動で拡張する**
- **認証（OIDC/SAML）や非同期処理（Celery）の API も OpenAPI に記述する**

このアプローチなら、**FastAPI の自動生成を活用しながら、OpenAPI の標準にも準拠できます！** 🚀