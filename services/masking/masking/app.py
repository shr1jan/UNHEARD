"""FastAPI surface for the masking service (skeleton).

The gateway streams raw bytes here; this service converts in-memory and returns
the masked buffer. Raw audio is never persisted. (ARCH-PIPE-01)
"""
from __future__ import annotations

from fastapi import FastAPI, Request, Response

from .convert import convert

app = FastAPI(title="unheard-masking", version="0.0.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/convert")
async def convert_endpoint(request: Request) -> Response:
    raw = await request.body()  # in-memory only
    masked = convert(raw)
    # raw goes out of scope here; nothing is written to disk or logs.
    return Response(content=masked, media_type="application/octet-stream")
