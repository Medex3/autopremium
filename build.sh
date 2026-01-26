#!/usr/bin/env bash
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сборка статических файлов
python manage.py collectstatic --no-input

# ПРИМЕНЕНИЕ МИГРАЦИЙ БАЗЫ ДАННЫХ - ключевой шаг!
python manage.py migrate
