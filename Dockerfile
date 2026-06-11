FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /app

#Copy requirements
COPY pyproject.toml uv.lock ./

#Install requirements
RUN uv sync --frozen --no-dev

#Copy other code
COPY . .

#Final image
FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#Copy .venv
COPY --from=builder /app/.venv /app/.venv

#Copy Alembic migrations
COPY --from=builder /app/alembic /app/alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini

#Copy src
COPY --from=builder /app/src /app/src

#Edit env path
ENV PATH="/app/.venv/bin:$PATH"

CMD sh -c "alembic upgrade head && uvicorn src.app.main:app --host 0.0.0.0 --port 8000"
