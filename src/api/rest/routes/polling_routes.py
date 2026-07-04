import logging

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import verify_opsadmin_or_reviewer_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/polling", tags=["polling"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.get("/status", dependencies=[Depends(verify_opsadmin_or_reviewer_role)])
async def get_polling_status(request: Request) -> Response:
    """Get the Gmail polling status (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/polling/status"
    return await proxy_request(request, target_url)


@router.post("/start", dependencies=[Depends(verify_opsadmin_or_reviewer_role)])
async def start_polling(request: Request) -> Response:
    """Start Gmail polling (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/polling/start"
    return await proxy_request(request, target_url)


@router.post("/stop", dependencies=[Depends(verify_opsadmin_or_reviewer_role)])
async def stop_polling(request: Request) -> Response:
    """Stop Gmail polling (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/polling/stop"
    return await proxy_request(request, target_url)
