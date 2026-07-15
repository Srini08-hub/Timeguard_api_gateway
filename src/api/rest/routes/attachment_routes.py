import logging

from fastapi import APIRouter, Request, Response

from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/attachments", tags=["attachments"])

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@router.get(
    "/{path:path}"
)
async def get_attachment(
    path: str,
    request: Request,
) -> Response:
    """Proxy attachment downloads through the gateway with reviewer access."""
    target_url = f"{settings.CORE_API_URL}/attachments/{path}"
    return await proxy_request(request, target_url)