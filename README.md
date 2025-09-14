# sentry-webhook

Sentry webhook receiver

1. Copy environment file:
   - `cp .env.example .env`
   - Fill `SENTRY_WEBHOOK_SECRET`
2. Run:
   - `docker compose up --build -d`
   - The app listens on `http://localhost:8001`.
3. Configure Sentry webhook endpoint to:
   - `POST http://<host>:8001/webhooks/sentry`
