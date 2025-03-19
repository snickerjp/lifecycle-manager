## **1. システム構成の概要**
シンプルでホストしやすい構成にしつつ、将来的なスケールも考慮。  
開発環境はDockerベース、認証はOkta＋OIDC/SAML対応。

### **構成イメージ**
```
┌────────────┐         ┌────────────┐
│  Frontend  │ ⇄ API  │  Backend   │
│ (React)    │ <----> │ (FastAPI?) │
└────────────┘         └────────────┘
        |                     |
        |                     |
        v                     v
 ┌────────────┐        ┌────────────┐
 │   Redis    │        │  Database  │
 │ (Cache)    │        │  (MySQL)   │
 └────────────┘        └────────────┘
```

### **各コンポーネントの役割**
- **Frontend (React, TypeScript, Material-UI)**
  - UI/UXを担当
  - API経由でバックエンドとやり取り

- **Backend (軽量なフレームワーク)**
  - REST APIまたはGraphQL APIを提供
  - 認証・認可 (OIDC/SAML)
  - EoLデータ取得バッチ
  - 製品・EoL・カテゴリ管理
  - 通知 (メール・Slack)
  - CSV入出力

- **Database (MySQL / SQLite)**
  - 製品・EoL情報・カテゴリ管理
  - ユーザーログ・通知履歴

- **Redis (Cache)**
  - フロントエンドのパフォーマンス向上
  - EoLデータの高速参照

- **CI/CD (GitHub Actions)**
  - Lint, Test, Build, Deployの自動化

---

## **2. 使用技術の選定**
### **バックエンドフレームワーク**
| 候補 | 特徴 | メリット | デメリット |
|------|------|--------|--------|
| **FastAPI (Python)** | 非同期API, 型安全 | 軽量・速い, Pythonエコシステム活用 | Python環境が必要 |
| **Express.js (Node.js)** | シンプルなAPI開発 | JavaScriptエコシステム利用可 | 非同期処理がやや面倒 |
| **NestJS (Node.js)** | TypeScript, DI, 高機能 | 型安全, 拡張性あり | Expressより学習コスト高 |
| **Spring Boot (Java)** | フルスタック, 大規模向け | 強力なエコシステム | 重め, Javaが必須 |

**→ FastAPIが良さそう**（軽量・高速・非同期で開発しやすい）

---

## **3. バッチ処理 (EoLデータ取得)**
### **処理概要**
1. `https://endoflife.date/` のAPIを1日1回取得
2. DBに保存
3. 失敗時はログに記録し、翌日リトライ

### **実装方法**
| 方法 | メリット | デメリット |
|------|--------|--------|
| **Celery + Redis (Python)** | 非同期処理に最適, 安定 | Celeryの管理が必要 |
| **Cron + Shell Script** | シンプル | 柔軟性が低い |
| **FastAPI Background Tasks** | 軽量, 簡単 | 高負荷時の管理が必要 |

**→ Celery + Redis を採用**（非同期処理＆タスク管理しやすい）

---

## **4. 認証・認可**
- **IdP: Okta**
- **認証方式: OpenID Connect (OIDC), SAML**
- **ユーザー管理**
  - Okta側でユーザー管理
  - APIリクエスト時にJWT検証

---

## **5. 通知 (メール・Slack)**
- **メール送信**
  - SendGrid or SESを利用
- **Slack通知**
  - Slack Webhookで送信
- **通知履歴**
  - データ量増加を考慮し、DBでなくログファイルに保存

---

### **まとめ**
- **バックエンド:** FastAPI (Python)
- **DB:** MySQL（初期はSQLite）
- **認証:** Okta (OIDC/SAML)
- **非同期処理:** Celery + Redis
- **通知:** SendGrid（メール）, Slack Webhook
- **CI/CD:** GitHub Actions
- **開発環境:** Docker, Docker Compose

---

`Poetry` に変更する場合、以下のような対応が必要です。

1. **`pyproject.toml` の作成**
   ```toml
   [tool.poetry]
   name = "lifecycle-manager"
   version = "0.1.0"
   description = "EoL & Maintenance Deadline Management System"
   authors = ["Your Name <your.email@example.com>"]

   [tool.poetry.dependencies]
   python = "^3.9"
   fastapi = "^0.95.0"
   uvicorn = "^0.21.0"
   celery = "^5.2.7"
   redis = "^4.3.4"
   mysql-connector-python = "^8.0.33"
   sqlalchemy = "^2.0.0"
   alembic = "^1.8.1"
   sendgrid = "^6.9.7"
   slack-sdk = "^3.21.3"
   ```

2. **`poetry.lock` の生成**
   ```sh
   poetry install
   ```

3. **Dockerfile の修正**
   ```dockerfile
   RUN poetry install --no-root
   ```

これで `requirements.txt` なしで依存関係を管理できます。  
他に `Poetry` に変更する際の細かい設定も必要であれば教えてください！