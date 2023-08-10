FROM python:3.9

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# pipenvのインストール
RUN pip install --no-cache-dir poetry

# ワーキングディレクトリの設定
WORKDIR /app
