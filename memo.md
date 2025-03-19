自社使用製品のEnd of Life管理システム

必要なもの：
- ユーザー管理機能（登録、ログイン、パスワード変更、退会）
    - IdP として Okta を利用する
    - 認証機能は、後にIdPを変更できるようにする
        - Oktaに依存しない形とする
    - OpenID Connect（OIDC）やSAMLをサポートする形にする
    - ロール機能は複雑になるので、実装しない
    - どのユーザーがどの製品を登録したかは、ログで残す

- 製品管理機能（製品の登録、編集、削除、一覧表示）
    - 個々の登録ではなく、OS、ミドルウェア(DB,Programing Language,Framework)、ネットワーク機器などを種別として登録
- カテゴリの登録、編集、紐付け
        - DEVELOPMENT
        - Operation
        - 1つの製品が複数カテゴリに紐づけられる仕様
        - カテゴリの登録、編集、削除は可能とする
- EoL管理機能（EoLの登録、編集、削除、一覧表示）
    - 製品と EoL は1対1の関係になるはず
    - OS、ミドルウェアのEOL情報はAPIから自動取得する
        - 更新頻度は、1日1回
        - 更新エラーの時は、エラーログを出力する
        - 更新エラーとなっても、更新前のデータを保持する
        - リトライは、翌日の実行で行う
        - https://endoflife.date/
        - Oracle JDK https://endoflife.date/api/oracle-jdk.json
        - CentOS https://endoflife.date/api/centos.json
        - 取得したデータは、DBに保存する
- ダッシュボード（製品ごとのEoL情報を一覧表示）
    - カテゴリ毎のフィルター表示
        - DEVELOPMENT
        - Operation
- 通知機能（EoLが近づいたら通知する）
    - メール通知
    - Slack通知
    - 通知タイミングは、EoL日の1ヶ月前がデフォルト、カスタマイズ可能
    - 通知頻度は、1ヶ月前、2週間前、1週間前、3日前、1日前
    - 通知の送信履歴を残す
        - DBに保存すると、データが増えるので、ログファイルに保存する
- ログ機能（ユーザーの操作ログを残す）
    - ログの内容
        - ユーザーID
        - 操作内容（製品登録、EoL登録、EoL更新、EoL削除）
        - 操作日時
- CSVエクスポート機能（製品、EoL情報をCSVでエクスポート）
- CSVインポート機能（製品、EoL情報をCSVでインポート）
    - CSVのフォーマット
        - 製品
            - 製品名（文字列）
            - 取引先会社（空欄可能）
            - EoL日（日付）
        - エンコードは、UTF-8
        - 日付フォーマットエラーはエラーとして表示
        - 重複データは差分表示を行い、ユーザーに選択させる
            - CSVの差分比較UI
            - CSVが元データなので、テーブル形式で表示して差分の箇所をハイライトする

技術要件：
デバッグが容易なものを選定する
Dockerで開発環境を構築する

- フロントエンド
    - React
    - TypeScript
    - Material-UI
- バックエンド
軽量でホストできるもの
- データベース
    - SQLite(小さいうちは)
    - MySQL
- Schema管理
    - Atlas https://atlasgo.io/
- Cache（画面表示）
    - Redis
- CI/CD
    - GitHub Actions
- テスト
    - Jest
    - React Testing Library
    - MySQLのテストは、Dockerで行う
- 開発、テスト環境
    - Docker
    - Docker Compose
    - MySQLもDockerで立ち上げる