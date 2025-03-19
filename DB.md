自社使用製品のEnd of Life（EoL）管理システムのデータベース設計について、以下のようなテーブル構成を提案します。この設計は、製品、EoL情報、カテゴリ、ユーザー操作ログなどを効率的に管理することを目的としています。

**1. 製品（products）テーブル**

| カラム名           | データ型     | 制約               | 説明                         |
|--------------------|--------------|--------------------|------------------------------|
| id                 | INTEGER      | PRIMARY KEY        | 製品の一意識別子             |
| name               | TEXT         | NOT NULL           | 製品名                       |
| vendor             | TEXT         |                    | 取引先会社（ベンダー）       |
| category_id        | INTEGER      |                    | カテゴリID（複数可）         |
| created_by_user_id | INTEGER      | NOT NULL           | 登録したユーザーのID         |
| created_at         | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 登録日時             |
| updated_at         | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 更新日時             |

**2. EoL情報（eol_info）テーブル**

| カラム名           | データ型     | 制約               | 説明                         |
|--------------------|--------------|--------------------|------------------------------|
| id                 | INTEGER      | PRIMARY KEY        | EoL情報の一意識別子          |
| product_id         | INTEGER      | NOT NULL, FOREIGN KEY REFERENCES products(id) | 対応する製品のID |
| eol_date           | DATE         | NOT NULL           | EoL日                        |
| source             | TEXT         |                    | EoL情報の取得元（例：API名） |
| created_at         | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 登録日時             |
| updated_at         | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 更新日時             |

**3. カテゴリ（categories）テーブル**

| カラム名   | データ型     | 制約        | 説明                 |
|------------|--------------|-------------|----------------------|
| id         | INTEGER      | PRIMARY KEY | カテゴリの一意識別子 |
| name       | TEXT         | NOT NULL    | カテゴリ名           |

**4. 製品とカテゴリの関連（product_categories）テーブル**

| カラム名    | データ型     | 制約        | 説明                         |
|-------------|--------------|-------------|------------------------------|
| product_id  | INTEGER      | NOT NULL, FOREIGN KEY REFERENCES products(id) | 製品のID |
| category_id | INTEGER      | NOT NULL, FOREIGN KEY REFERENCES categories(id) | カテゴリのID |

**5. ユーザー操作ログ（user_logs）テーブル**

| カラム名   | データ型     | 制約        | 説明                         |
|------------|--------------|-------------|------------------------------|
| id         | INTEGER      | PRIMARY KEY | ログの一意識別子             |
| user_id    | INTEGER      | NOT NULL    | 操作を行ったユーザーのID     |
| action     | TEXT         | NOT NULL    | 操作内容（例：製品登録、EoL更新） |
| details    | TEXT         |             | 操作の詳細情報               |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 操作日時             |

**6. 通知履歴（notification_logs）テーブル**

| カラム名     | データ型     | 制約        | 説明                         |
|--------------|--------------|-------------|------------------------------|
| id           | INTEGER      | PRIMARY KEY | 通知履歴の一意識別子         |
| product_id   | INTEGER      | NOT NULL, FOREIGN KEY REFERENCES products(id) | 対象製品のID |
| notification_type | TEXT    | NOT NULL    | 通知の種類（メール、Slackなど） |
| sent_at      | TIMESTAMP    | NOT NULL    | 通知送信日時                 |

**7. ユーザー（users）テーブル**

| カラム名   | データ型     | 制約        | 説明                         |
|------------|--------------|-------------|------------------------------|
| id         | INTEGER      | PRIMARY KEY | ユーザーの一意識別子         |
| username   | TEXT         | NOT NULL    | ユーザー名                   |
| email      | TEXT         | NOT NULL    | メールアドレス               |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 登録日時             |
| updated_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | 更新日時             |

**APIから取得するデータの構造**

`https://endoflife.date/api/oracle-jdk.json` から取得できるデータは、以下のようなJSON形式です：

```json
[
  {
    "cycle": "21",
    "releaseDate": "2021-09-14",
    "eol": false,
    "latest": "21.0.0",
    "latestReleaseDate": "2021-09-14",
    "link": "https://www.oracle.com/java/technologies/javase/jdk21-support-roadmap.html"
  },
  ...
]
```

このデータを取り込む際には、`cycle`（バージョン）、`releaseDate`（リリース日）、`eol`（EoLステータス）、`latest`（最新バージョン）、`latestReleaseDate`（最新リリース日）、`link`（詳細情報のリンク）などの情報を `eol_info` テーブルに適切にマッピングします。

このデータベース設計により、製品とそのEoL情報、カテゴリ、ユーザー操作ログ、通知履歴などを効率的に管理できると考えます。 

ご要望の自社使用製品のEnd of Life（EoL）管理システムに必要なデータベースのテーブル設計を、AtlasのHCL形式で提案いたします。以下の設計では、製品、EoL、カテゴリ、ユーザー、操作ログの各テーブルを定義しています。

```hcl
schema "eol_management" {
}

table "users" {
  schema = schema.eol_management
  column "id" {
    type = int
    null = false
    auto_increment = true
  }
  column "username" {
    type = varchar(255)
    null = false
    unique = true
  }
  column "email" {
    type = varchar(255)
    null = false
    unique = true
  }
  column "password_hash" {
    type = varchar(255)
    null = false
  }
  column "created_at" {
    type = timestamp
    null = false
    default = "CURRENT_TIMESTAMP"
  }
  primary_key {
    columns = [column.id]
  }
}

table "categories" {
  schema = schema.eol_management
  column "id" {
    type = int
    null = false
    auto_increment = true
  }
  column "name" {
    type = varchar(255)
    null = false
    unique = true
  }
  primary_key {
    columns = [column.id]
  }
}

table "products" {
  schema = schema.eol_management
  column "id" {
    type = int
    null = false
    auto_increment = true
  }
  column "name" {
    type = varchar(255)
    null = false
  }
  column "vendor" {
    type = varchar(255)
    null = true
  }
  column "category_id" {
    type = int
    null = false
  }
  column "created_by" {
    type = int
    null = false
  }
  column "created_at" {
    type = timestamp
    null = false
    default = "CURRENT_TIMESTAMP"
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "fk_category" {
    columns = [column.category_id]
    ref_columns = [table.categories.column.id]
  }
  foreign_key "fk_user" {
    columns = [column.created_by]
    ref_columns = [table.users.column.id]
  }
}

table "eol_info" {
  schema = schema.eol_management
  column "id" {
    type = int
    null = false
    auto_increment = true
  }
  column "product_id" {
    type = int
    null = false
  }
  column "eol_date" {
    type = date
    null = false
  }
  column "retrieved_from_api" {
    type = boolean
    null = false
    default = false
  }
  column "created_at" {
    type = timestamp
    null = false
    default = "CURRENT_TIMESTAMP"
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "fk_product" {
    columns = [column.product_id]
    ref_columns = [table.products.column.id]
  }
}

table "product_categories" {
  schema = schema.eol_management
  column "product_id" {
    type = int
    null = false
  }
  column "category_id" {
    type = int
    null = false
  }
  primary_key {
    columns = [column.product_id, column.category_id]
  }
  foreign_key "fk_product" {
    columns = [column.product_id]
    ref_columns = [table.products.column.id]
  }
  foreign_key "fk_category" {
    columns = [column.category_id]
    ref_columns = [table.categories.column.id]
  }
}

table "operation_logs" {
  schema = schema.eol_management
  column "id" {
    type = int
    null = false
    auto_increment = true
  }
  column "user_id" {
    type = int
    null = false
  }
  column "operation" {
    type = varchar(255)
    null = false
  }
  column "details" {
    type = text
    null = true
  }
  column "created_at" {
    type = timestamp
    null = false
    default = "CURRENT_TIMESTAMP"
  }
  primary_key {
    columns = [column.id]
  }
  foreign_key "fk_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
  }
}
```

**テーブル説明:**

- **users**: ユーザー情報を管理します。ユーザー名、メールアドレス、パスワードハッシュ、作成日時を保持します。

- **categories**: 製品のカテゴリ情報を管理します。カテゴリ名を保持します。

- **products**: 製品情報を管理します。製品名、ベンダー、関連するカテゴリID、作成者ユーザーID、作成日時を保持します。

- **eol_info**: 各製品のEoL情報を管理します。製品ID、EoL日付、APIから取得したかどうかのフラグ、作成日時を保持します。

- **product_categories**: 製品とカテゴリの多対多の関係を管理します。製品IDとカテゴリIDの組み合わせを保持します。

- **operation_logs**: ユーザーの操作ログを管理します。ユーザーID、操作内容、詳細、作成日時を保持します。

この設計により、製品とカテゴリの多対多の関係や、ユーザーの操作履歴の追跡が可能となります。また、EoL情報は製品ごとに一意に関連付けられ、APIから取得したデータかどうかを識別できます。

なお、CSVインポート機能や通知履歴の保存方法については、要件に応じて別途テーブルを設計することをおすすめします。特に、通知履歴をログファイルに保存する場合は、ファイルシステムの構成やログローテーションのポリシーも検討してください。 