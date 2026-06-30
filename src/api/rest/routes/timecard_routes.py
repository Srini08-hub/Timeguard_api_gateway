import logging
import uuid

from fastapi import APIRouter, Depends, Request, Response

from src.api.rest.dependencies import verify_reviewer_role
from src.config.settings import settings
from src.utils.proxy import proxy_request

router = APIRouter(prefix="/timecards", tags=["timecards"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@router.get(
    "/timesheet/{timesheet_id}",
    dependencies=[Depends(verify_reviewer_role)],
)
async def get_timecards_by_timesheet(
    timesheet_id: uuid.UUID,
    request: Request,
) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/timesheet/{timesheet_id}"
    return await proxy_request(request, target_url)


@router.get(
    "/approved/export",
    dependencies=[Depends(verify_reviewer_role)],
)
async def export_approved_timecards(request: Request) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/approved/export"
    return await proxy_request(request, target_url)


@router.get(
    "/approved",
    dependencies=[Depends(verify_reviewer_role)],
)
async def get_approved_timecards(request: Request) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/approved"
    return await proxy_request(request, target_url)


@router.get(
    "/rejected",
    dependencies=[Depends(verify_reviewer_role)],
)
async def get_rejected_timecards(request: Request) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/rejected"
    return await proxy_request(request, target_url)


@router.patch(
    "/bulk/approve",
    dependencies=[Depends(verify_reviewer_role)],
)
async def approve_timecards(request: Request) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/bulk/approve"
    return await proxy_request(request, target_url)


@router.get(
    "/{timecard_id}",
    dependencies=[Depends(verify_reviewer_role)],
)
async def get_timecard(
    timecard_id: uuid.UUID,
    request: Request,
) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/{timecard_id}"
    return await proxy_request(request, target_url)


@router.patch(
    "/{timecard_id}/resolve",
    dependencies=[Depends(verify_reviewer_role)],
)
async def resolve_timecard(
    timecard_id: uuid.UUID,
    request: Request,
) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/{timecard_id}/resolve"
    return await proxy_request(request, target_url)


@router.patch(
    "/{timecard_id}/approve",
    dependencies=[Depends(verify_reviewer_role)],
)
async def approve_timecard(
    timecard_id: uuid.UUID,
    request: Request,
) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/{timecard_id}/approve"
    return await proxy_request(request, target_url)


@router.patch(
    "/{timecard_id}/reject",
    dependencies=[Depends(verify_reviewer_role)],
)
async def reject_timecard(
    timecard_id: uuid.UUID,
    request: Request,
) -> Response:
    target_url = f"{settings.CORE_API_URL}/timecards/{timecard_id}/reject"
    return await proxy_request(request, target_url)
