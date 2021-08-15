# ベースイメージ
FROM python:3.5.9

# pipをアップグレード
RUN pip install --upgrade pip

# 作業ディレクトリ作成
WORKDIR /workdir

# ポート
EXPOSE 8080


