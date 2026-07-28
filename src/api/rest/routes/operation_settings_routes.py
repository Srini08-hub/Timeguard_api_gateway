from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import verify_opsadmin_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get(
    "/excel-extraction-strategy",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def get_excel_extraction_strategy(request: Request) -> Response:
    """Get Excel extraction strategy settings from core backend."""
    target_url = f"{settings.CORE_API_URL}/operations/excel-extraction-strategy"
    return await proxy_request(request, target_url)


@router.patch(
    "/excel-extraction-strategy",
    dependencies=[Depends(verify_opsadmin_role)],
)
async def update_excel_extraction_strategy(request: Request) -> Response:
    """Update Excel extraction strategy settings in core backend."""
    target_url = f"{settings.CORE_API_URL}/operations/excel-extraction-strategy"
    return await proxy_request(request, target_url)