import logging
import uuid

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import (
    verify_opsadmin_or_reviewer_role,
    verify_opsadmin_role,
)
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/departments", tags=["departments"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.post(
    "",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def create_department(request: Request) -> Response:
    """Create department (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/departments"
    return await proxy_request(request, target_url)


@router.get(
    "/client/{client_id}",
    dependencies=[Depends(verify_opsadmin_or_reviewer_role)],
)
async def get_departments_by_client(
    client_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get departments by client (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/departments/client/{client_id}"
    return await proxy_request(request, target_url)


@router.get(
    "/{department_id}",
    dependencies=[Depends(verify_opsadmin_or_reviewer_role)],
)
async def get_department(
    department_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get department by ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/departments/{department_id}"
    return await proxy_request(request, target_url)


@router.patch(
    "/{department_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def update_department(
    department_id: uuid.UUID,
    request: Request,
) -> Response:
    """Update department (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/departments/{department_id}"
    return await proxy_request(request, target_url)


@router.delete(
    "/{department_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def delete_department(
    department_id: uuid.UUID,
    request: Request,
) -> Response:
    """Delete department (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/departments/{department_id}"
    return await proxy_request(request, target_url)
