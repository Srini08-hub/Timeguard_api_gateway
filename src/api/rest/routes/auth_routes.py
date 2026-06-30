import logging
from typing import cast

import httpx
from fastapi import APIRouter, Cookie, Request, Response, status
from fastapi.responses import JSONResponse

from src.config.settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=None, status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    response: Response,
) -> dict[str, str] | JSONResponse:
    """Forward login credentials, set cookies on success, and return user info."""
    target_url = f"{settings.AUTH_URL}/auth/login"
    client: httpx.AsyncClient = request.app.state.http_client

    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }
    body = await request.body()

    try:
        backend_response = await client.post(
            target_url,
            headers=headers,
            content=body,
        )
    except httpx.RequestError as exc:
        return JSONResponse(
            content={"detail": f"Gateway routing error: {str(exc)}"},
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    if backend_response.status_code != status.HTTP_200_OK:
        try:
            err_content = backend_response.json()
        except ValueError:
            err_content = {"detail": backend_response.text}
        return JSONResponse(
            content=err_content,
            status_code=backend_response.status_code,
        )

    data = backend_response.json()
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    user_info = data.get("user", {})
    logger.info(data)
    if access_token:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAME_SITE,
            max_age=settings.COOKIE_ACCESS_MAX_AGE,
            path="/",
        )
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAME_SITE,
            max_age=settings.COOKIE_REFRESH_MAX_AGE,
            path="/",
        )

    # Prevent browsers from caching auth responses
    response.headers["Cache-Control"] = "no-store"

    return cast(dict[str, str], user_info)


@router.post("/refresh", response_model=None, status_code=status.HTTP_200_OK)
async def refresh(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
) -> dict[str, str] | JSONResponse:
    """Take refresh token from cookies, call downstream refresh, and update cookies."""
    if not refresh_token:
        return JSONResponse(
            content={"detail": "Refresh token missing"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    target_url = f"{settings.AUTH_URL}/auth/refresh"
    client: httpx.AsyncClient = request.app.state.http_client

    try:
        backend_response = await client.post(
            target_url,
            cookies={"refresh_token": refresh_token},
        )
    except httpx.RequestError as exc:
        return JSONResponse(
            content={"detail": f"Gateway routing error: {str(exc)}"},
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    if backend_response.status_code != status.HTTP_200_OK:
        try:
            err_content = backend_response.json()
        except ValueError:
            err_content = {"detail": backend_response.text}
        return JSONResponse(
            content=err_content,
            status_code=backend_response.status_code,
        )

    data = backend_response.json()
    new_access_token = data.get("access_token")
    new_refresh_token = data.get("refresh_token")
    logger.info(new_access_token)

    if new_access_token and new_refresh_token:
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAME_SITE,
            max_age=settings.COOKIE_ACCESS_MAX_AGE,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAME_SITE,
            max_age=settings.COOKIE_REFRESH_MAX_AGE,
            path="/",
        )

    # Prevent browsers from caching auth responses
    response.headers["Cache-Control"] = "no-store"

    return {"message": "Tokens refreshed successfully"}


@router.post("/logout", response_model=None, status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
) -> dict[str, str] | JSONResponse:
    """Validate access token, forward logout to revoke session, and clear cookies."""

    # # Validate the access token before proceeding
    # if not access_token:
    #     return JSONResponse(
    #         content={"detail": "Not authenticated"},
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #     )
    if not refresh_token:
        return JSONResponse(
            content={"detail": "Refresh token missing"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # payload = decode_access_token(refresh_token)
    # if not payload:
    #     # Token is invalid or expired — still clear cookies so client is cleaned up
    #     response.delete_cookie(key="access_token", path="/")
    #     response.delete_cookie(key="refresh_token", path="/")
    #     return JSONResponse(
    #         content={"detail": "Invalid or expired token"},
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #     )

    target_url = f"{settings.AUTH_URL}/auth/logout"
    client: httpx.AsyncClient = request.app.state.http_client

    try:
        await client.post(
            target_url,
            cookies={"refresh_token": refresh_token},
        )
    except httpx.RequestError as exc:
        return JSONResponse(
            content={"detail": f"Gateway routing error: {str(exc)}"},
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    # Always clear gateway cookies regardless of downstream response
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")

    return {"message": "Logged out successfully"}
