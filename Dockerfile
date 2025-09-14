FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8001
CMD ["uv", "run", "granian", "--interface", "asgi", "sentry-webhook.app:app", "--host", "0.0.0.0", "--port", "8001"]
