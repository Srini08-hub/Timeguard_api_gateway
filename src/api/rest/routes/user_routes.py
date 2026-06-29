import logging

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import (
    get_current_user_claims,
    verify_admin_role,
)
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/users",tags=["users"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



@router.get("/me")
async def get_user_me(
    request: Request,
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> Response:
    """Get current user information (proxied to auth backend)."""
    target_url = f"{settings.AUTH_URL}/users/me"
    return await proxy_request(request, target_url)


@router.get("", dependencies=[Depends(verify_admin_role)])
async def get_users(request: Request) -> Response:
    """Get all users (admin only, proxied to auth backend)."""
    target_url = f"{settings.AUTH_URL}/users"
    return await proxy_request(request, target_url)


@router.post("", dependencies=[Depends(verify_admin_role)])
async def create_user(request: Request) -> Response:
    """Create a new user (admin only, proxied to auth backend)."""
    target_url = f"{settings.AUTH_URL}/users"
    return await proxy_request(request, target_url)


@router.patch("/{user_id}", dependencies=[Depends(verify_admin_role)])
async def patch_user(
    user_id: str,
    request: Request,
) -> Response:
    """Update a user by ID (admin only, proxied to auth backend)."""
    target_url = f"{settings.AUTH_URL}/users/{user_id}"
    return await proxy_request(request, target_url)


@router.delete("/{user_id}", dependencies=[Depends(verify_admin_role)])
async def delete_user(
    user_id: str,
    request: Request,
) -> Response:
    """Delete a user by ID (admin only, proxied to auth backend)."""
    target_url = f"{settings.AUTH_URL}/users/{user_id}"
    return await proxy_request(request, target_url)
