import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import (
    get_current_user_claims,
    verify_opsadmin_role,
)
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/employees", tags=["employees"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.post("", dependencies=[Depends(verify_opsadmin_role)])
async def create_employee(
    request: Request,
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> Response:
    """Create employee (proxied to core backend)."""
    payload = await request.json()
    payload["created_by"] = claims["sub"]

    target_url = f"{settings.CORE_API_URL}/employees"
    return await proxy_request(request, target_url, json_body=payload)


@router.get("/active")
async def get_active_employees(
    request: Request,
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> Response:
    """Get active employees (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/employees/active"
    return await proxy_request(request, target_url)

@router.get("/inactive")
async def get_inactive_employees(
    request: Request,
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> Response:
    """Get inactive employees (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/employees/inactive"
    return await proxy_request(request, target_url)


@router.get("/unassigned")
async def get_unassigned_employees(
    request: Request,
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> Response:
    """Get unassigned employees (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/employees/unassigned"
    return await proxy_request(request, target_url)

@router.get("/{emp_id}")
async def get_employee(
    emp_id: UUID,
    request: Request,
    claims: dict[str, str] = Depends(get_current_user_claims),
) -> Response:
    """Get employee by ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/employees/{emp_id}"
    return await proxy_request(request, target_url)


@router.put("/{emp_id}", dependencies=[Depends(verify_opsadmin_role)])
async def update_employee(
    emp_id: UUID,
    request: Request,
) -> Response:
    """Update employee by ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/employees/{emp_id}"
    return await proxy_request(request, target_url)


@router.delete("/{emp_id}", dependencies=[Depends(verify_opsadmin_role)])
async def soft_delete_employee(
    emp_id: UUID,
    request: Request,
) -> Response:
    """Soft delete employee by ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/employees/{emp_id}"
    return await proxy_request(request, target_url)
