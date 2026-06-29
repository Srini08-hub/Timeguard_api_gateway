import logging

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import verify_reviewer_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/content-extracts", tags=["content-extracts"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@router.get("/email/{email_id}", dependencies=[Depends(verify_reviewer_role)])
async def get_content_extracts_by_email_id(
    email_id: str,
    request: Request,
) -> Response:
    """Get content extracts by email ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/content-extracts/email/{email_id}"
    return await proxy_request(request, target_url)
