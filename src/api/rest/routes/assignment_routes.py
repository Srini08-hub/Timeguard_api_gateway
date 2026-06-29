import logging
import uuid

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import verify_opsadmin_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/assignments", tags=["assignments"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.post(
    "",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def create_assignment(request: Request) -> Response:
    """Create assignments (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/assignments"
    return await proxy_request(request, target_url)


@router.get(
    "/employee/{emp_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def get_assignments_by_employee(
    emp_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get assignments by employee (proxied to core backend)."""
    target_url = (
        f"{settings.CORE_API_URL}/assignments/employee/{emp_id}"
    )
    return await proxy_request(request, target_url)


@router.get(
    "/client/{client_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def get_assignments_by_client(
    client_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get assignments by client (proxied to core backend)."""
    target_url = (
        f"{settings.CORE_API_URL}/assignments/client/{client_id}"
    )
    return await proxy_request(request, target_url)


@router.get(
    "/department/{department_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def get_assignments_by_department(
    department_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get assignments by department (proxied to core backend)."""
    target_url = (
        f"{settings.CORE_API_URL}/assignments/department/{department_id}"
    )
    return await proxy_request(request, target_url)


@router.get(
    "/{assignment_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def get_assignment(
    assignment_id: uuid.UUID,
    request: Request,
) -> Response:
    """Get assignment by ID (proxied to core backend)."""
    target_url = (
        f"{settings.CORE_API_URL}/assignments/{assignment_id}"
    )
    return await proxy_request(request, target_url)


@router.patch(
    "/{assignment_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def update_assignment(
    assignment_id: uuid.UUID,
    request: Request,
) -> Response:
    """Update assignment (proxied to core backend)."""
    target_url = (
        f"{settings.CORE_API_URL}/assignments/{assignment_id}"
    )
    return await proxy_request(request, target_url)


@router.delete(
    "/{assignment_id}",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def delete_assignment(
    assignment_id: uuid.UUID,
    request: Request,
) -> Response:
    """Delete assignment (proxied to core backend)."""
    target_url = (
        f"{settings.CORE_API_URL}/assignments/{assignment_id}"
    )
    return await proxy_request(request, target_url)