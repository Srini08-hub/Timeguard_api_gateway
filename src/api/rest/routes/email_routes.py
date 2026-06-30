import logging

from fastapi import APIRouter, Depends, Query, Request, Response

from src.api.rest.dependencies import verify_reviewer_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

# from urllib.parse import urlencode

router = APIRouter(prefix="/emails", tags=["emails"])

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@router.get("/timesheet-emails", dependencies=[Depends(verify_reviewer_role)])
async def get_timesheet_emails(request: Request) -> Response:
    """Get all timesheet emails (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/emails/timesheet-emails"
    return await proxy_request(request, target_url)


@router.get("/non-timesheet-emails", dependencies=[Depends(verify_reviewer_role)])
async def get_non_timesheet_emails(request: Request) -> Response:
    """Get all non-timesheet emails (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/emails/non-timesheet-emails"
    return await proxy_request(request, target_url)


@router.get("", dependencies=[Depends(verify_reviewer_role)])
async def get_emails_by_status(
    request: Request,
    status: str = Query(...),
) -> Response:
    target_url = f"{settings.CORE_API_URL}/emails?status={status}"
    return await proxy_request(request, target_url)


@router.get("/{email_id}/attachments", dependencies=[Depends(verify_reviewer_role)])
async def get_attachments(
    email_id: str,
    request: Request,
) -> Response:
    """Get email attachments by email ID (proxied to core backend)."""
    target_url = f"{settings.CORE_API_URL}/emails/{email_id}/attachments"
    return await proxy_request(request, target_url)
