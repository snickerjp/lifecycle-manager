FROM python:3.9-slim

WORKDIR /app

# システムの依存関係とPoetryのインストール
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

# PATHにPoetryを追加
ENV PATH="/root/.local/bin:$PATH"

# Poetry の設定（venv を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係のインストール
COPY pyproject.toml poetry.lock* ./
RUN poetry install --without dev --no-root

# アプリケーションのコピー
COPY . .

# アプリケーションの起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]