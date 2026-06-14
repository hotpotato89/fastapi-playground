# FastAPI Playground

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![Docker](https://img.shields.io/badge/Docker-28-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Alembic](https://img.shields.io/badge/Alembic-1.14-orange)
![Nginx](https://img.shields.io/badge/Nginx-1.27-green)

Production-ready REST API с JWT аутентификацией, refresh токенами, Docker и Nginx.

## Технологии

- Python 3.14 / FastAPI
- PostgreSQL 18 / SQLAlchemy 2.0
- JWT (RS256) / Argon2
- Docker / Docker Compose
- Nginx

# Быстрый старт

## Клонирование:

```bash
git clone https://github.com/hotpotato89/fastapi-playground.git
cd fastapi-playground
```

## Настройка окружения:
```bash
cp .env.example .env
```

## Генерация RSA ключей:
```bash
mkdir -p keys
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem
```

## Запуск:
```bash
docker compose up -d --build
```

## Проверка:
```bash
curl http://localhost/api/health
```

# API Эндпоинты

Аутентификация:
- POST /api/auth/register - регистрация
- POST /api/auth/login - логин (access + refresh)
- POST /api/auth/refresh - обновить access
- POST /api/auth/logout - выход
- GET /api/auth/me - профиль

Книги:
- POST /api/book/ - создать (требует токен)
- GET /api/book/ - список (пагинация, фильтры)
- GET /api/book/{id} - получить
- PATCH /api/book/{id} - обновить (владелец)
- DELETE /api/book/{id} - удалить (владелец)

Документация:
- /docs - Swagger UI
- /openapi.json - OpenAPI схема

# Docker команды

## Запуск всех сервисов:
```bash
docker compose up -d --build
```

## Просмотр логов:
```bash
docker compose logs -f
```

## Остановка:
```bash
docker compose down
```

## Полная очистка (с удалением данных):
```bash
docker compose down -v
```

# Переменные окружения (.env)

 - DB__NAME=playground_db
 - DB__USER=postgres
 - DB__PASSWORD=your_password
 - DB__HOST=db
 - DB__PORT=5432

 - JWT__ALGORITHM=RS256
 - JWT__PRIVATE_KEY_PATH=keys/private.pem
 - JWT__PUBLIC_KEY_PATH=keys/public.pem

 - DEPLOY__ALLOW_ORIGINS=["http://localhost"]
 - DEPLOY__ALLOW_CREDENTIALS=true
 - DEPLOY__ALLOW_HEADERS=["*"]
 - DEPLOY__ALLOW_METHODS=["*"]

# Особенности безопасности

- JWT access (15 минут) + refresh (7 дней)
- RSA подпись токенов (асимметричное шифрование)
- Argon2 хэширование паролей
- Чистая архитектура (Service → Repository)
- Nginx reverse proxy + раздача статики