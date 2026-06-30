import logging
import uuid

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import (
    verify_opsadmin_or_reviewer_role,
    verify_opsadmin_role,
)
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/clients", tags=["clients"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.post(
    "",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def create_client(request: Request) -> Response:
    """Create a client (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/clients"
    return await proxy_request(request, target_url)


@router.get(
    "",
    dependencies=[Depends(verify_opsadmin_or_reviewer_role)],
)
async def get_active_clients(request: Request) -> Response:
    """Get active clients (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/clients"
    return await proxy_request(request, target_url)


@router.patch(
    "/{client_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def update_client(
    client_id: uuid.UUID,
    request: Request,
) -> Response:
    """Update client (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/clients/{client_id}"
    return await proxy_request(request, target_url)


@router.delete(
    "/{client_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def soft_delete_client(
    client_id: uuid.UUID,
    request: Request,
) -> Response:
    """Soft delete client (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/clients/{client_id}"
    return await proxy_request(request, target_url)
