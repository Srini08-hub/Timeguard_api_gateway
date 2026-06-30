import logging
import uuid

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import (
    verify_opsadmin_or_reviewer_role,
    verify_opsadmin_role,
)
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/client-rules", tags=["client-rules"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.post(
    "",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def create_rule(request: Request) -> Response:
    """Create client rule (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/client-rules"
    return await proxy_request(request, target_url)


@router.get(
    "/department/{department_id}",
    dependencies=[Depends(verify_opsadmin_or_reviewer_role)],
)
async def get_rules_by_department(
    department_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get client rules by department (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/client-rules/department/{department_id}"
    return await proxy_request(request, target_url)


@router.get(
    "/{rule_id}",
    dependencies=[Depends(verify_opsadmin_or_reviewer_role)],
)
async def get_rule(
    rule_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get client rule by ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/client-rules/{rule_id}"
    return await proxy_request(request, target_url)


@router.patch(
    "/{rule_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def update_rule(
    rule_id: uuid.UUID,
    request: Request,
) -> Response:
    """Update client rule (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/client-rules/{rule_id}"
    return await proxy_request(request, target_url)


@router.delete(
    "/{rule_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def soft_delete_rule(
    rule_id: uuid.UUID,
    request: Request,
) -> Response:
    """Soft delete client rule (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/client-rules/{rule_id}"
    return await proxy_request(request, target_url)