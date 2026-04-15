#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/opt/microservices-ecommerce"
ENV_FILE="$PROJECT_DIR/.env.prod"
SQL_FILE="$PROJECT_DIR/reset-stocks.sql"
CONTAINER_NAME="mysql"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Fichier .env.prod introuvable : $ENV_FILE"
  exit 1
fi

if [[ ! -f "$SQL_FILE" ]]; then
  echo "Fichier SQL introuvable : $SQL_FILE"
  exit 1
fi

MYSQL_ROOT_PASSWORD="$(grep '^MYSQL_ROOT_PASSWORD=' "$ENV_FILE" | cut -d '=' -f2-)"
MYSQL_DATABASE="$(grep '^MYSQL_DATABASE=' "$ENV_FILE" | cut -d '=' -f2-)"

if [[ -z "${MYSQL_ROOT_PASSWORD:-}" || -z "${MYSQL_DATABASE:-}" ]]; then
  echo "Impossible de lire MYSQL_ROOT_PASSWORD ou MYSQL_DATABASE dans $ENV_FILE"
  exit 1
fi

echo "Reset des stocks dans la base $MYSQL_DATABASE..."

docker exec -i "$CONTAINER_NAME" mysql -uroot "-p$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < "$SQL_FILE"

echo "Stocks réinitialisés avec succès."
