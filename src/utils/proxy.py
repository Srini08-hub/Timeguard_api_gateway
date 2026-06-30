import logging
from typing import Any

import httpx
from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def proxy_request(
    request: Request,
    target_url: str,
    json_body: dict[str, Any] | None = None,
) -> Response:
    """Proxy an incoming request to a target downstream service."""
    client: httpx.AsyncClient = request.app.state.http_client

    # Prepare headers (excluding Host and Content-Length)
    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }

    body = await request.body() if json_body is None else None

    try:
        # Perform the downstream HTTP request
        backend_response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=dict(request.query_params),
            content=body,
            json=json_body,
        )
    except httpx.RequestError as exc:
        logger.error(f"Failed to route request to {target_url}: {exc}")
        return Response(
            content=f"Gateway error: Failed to route to downstream service. {str(exc)}",
            status_code=502,
        )

    # Clean response headers
    excluded_headers = {
        "content-length",
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
        "set-cookie",  # Set-Cookie is handled manually
    }

    response_headers = {
        k: v
        for k, v in backend_response.headers.items()
        if k.lower() not in excluded_headers
    }

    # Create Gateway response
    gateway_response = Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=response_headers,
    )

    # Forward any Set-Cookie headers from downstream

    return gateway_response
