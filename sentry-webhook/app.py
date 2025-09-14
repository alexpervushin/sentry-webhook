import hashlib
import hmac
import os

from faststream.nats import NatsBroker
from litestar import Litestar, Request, post

SENTRY_WEBHOOK_SECRET = os.getenv("SENTRY_WEBHOOK_SECRET", "")
SENTRY_NATS_SUBJECT = os.getenv("SENTRY_NATS_SUBJECT", "sentry.events")

broker = NatsBroker(os.getenv("NATS_URL", "nats://nats:4222"))


@post("/webhooks/sentry")
async def sentry_webhook(request: Request, body: bytes) -> None:
    sig = request.headers.get("sentry-hook-signature")
    if (
        sig
        and SENTRY_WEBHOOK_SECRET
        and hmac.compare_digest(
            hmac.new(SENTRY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest(),
            sig,
        )
    ):
        await broker.publish(body, subject=SENTRY_NATS_SUBJECT)


app = Litestar([sentry_webhook], on_startup=[broker.start], on_shutdown=[broker.close])
