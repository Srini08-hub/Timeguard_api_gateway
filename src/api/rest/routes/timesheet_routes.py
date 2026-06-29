import logging

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import verify_reviewer_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/timesheet", tags=["timesheet"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.get("/under_review", dependencies=[Depends(verify_reviewer_role)])
async def get_under_review_timesheets(request: Request) -> Response:
    target_url = f"{settings.CORE_API_URL}/timesheet/under_review"
    return await proxy_request(request, target_url)


@router.get("/processed", dependencies=[Depends(verify_reviewer_role)])
async def get_processed_timesheets(request: Request) -> Response:
    target_url = f"{settings.CORE_API_URL}/timesheet/processed"
    return await proxy_request(request, target_url)
