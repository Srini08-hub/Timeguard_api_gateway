"""Gateway security utilities."""

from typing import cast

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from src.config.settings import settings
from src.core.exceptions.custom_exeption import UnauthorizedException


def decode_access_token(token: str | None) -> dict[str, str]:
    """Decode and validate a raw JWT access token string.

    Raises ``UnauthorizedException`` if the token is missing, malformed,
    expired, or is missing required claims.
    """

    if not token:
        raise UnauthorizedException("Access token is missing")

    try:
        payload = cast(
            dict[str, str],
            jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            ),
        )
    except ExpiredSignatureError as exc:
        raise UnauthorizedException("Token expired") from exc
    except JWTError as exc:
        raise UnauthorizedException("Invalid token") from exc

    if not payload.get("sub") or not payload.get("role"):
        raise UnauthorizedException("Invalid token claims.")

    return payload
