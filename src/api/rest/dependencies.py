import logging

from fastapi import Cookie, Depends

from src.core.exceptions.custom_exeption import (
    ForbiddenException,
    UnauthorizedException,
)
from src.utils.security import decode_access_token

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_token(
    access_token: str | None = Cookie(default=None),
) -> str:
    """Extract and return access token from cookies, or raise UnauthorizedException."""
    logger.info(f"Extracted access token from cookie: {access_token}")
    # if not access_token:
    #     access_token = request.cookies.get("access_token")
    if not access_token:
        raise UnauthorizedException("Access token is missing")
    return access_token


def get_current_user_claims(token: str = Depends(get_token)) -> dict[str, str]:
    """Decode access token and return claims."""
    return decode_access_token(token)


def verify_admin_role(
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> None:
    """Verify that the user has the admin role, or raise ForbiddenException."""
    if claims.get("role") != "admin":
        raise ForbiddenException("Access denied. Admin role required.")


def verify_opsadmin_role(
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> None:
    """Verify that the user has the opsadmin role, or raise ForbiddenException."""
    if claims.get("role") != "OpsAdmin":
        raise ForbiddenException("Access denied. OpsAdmin role required.")


def verify_reviewer_role(
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> None:
    """Verify that the user has the reviewer role, or raise ForbiddenException."""
    if claims.get("role") != "reviewer":
        raise ForbiddenException("Access denied. Reviewer role required.")


def verify_opsadmin_or_reviewer_role(
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> None:
    """Verify OpsAdmin or reviewer role for read-only operational views."""
    if claims.get("role") not in ("OpsAdmin", "reviewer"):
        raise ForbiddenException("Access denied. OpsAdmin or reviewer role required.")
