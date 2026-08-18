#!/usr/bin/env bash
set -e

if ! grep -q "^API_KEY=" .env; then
    echo 'Error: API_KEY is not set in .env! Please add the line: API_KEY="demo"'
    exit 1
fi

echo "Starting PostgreSQL container..."
docker rm -f pg_cafe_db_container
docker compose up -d --remove-orphans

echo "Installing dependencies..."
uv sync

echo "Running migrations..."
uv run python manage.py makemigrations
uv run python manage.py migrate

echo "Seeding menu items..."
uv run python manage.py seed_menu_items

echo "All done! You can now run the server with:"
echo "uv run python manage.py runserver"
