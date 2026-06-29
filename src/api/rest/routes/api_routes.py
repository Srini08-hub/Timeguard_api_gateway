# from fastapi import APIRouter, Depends, Request, Response

# from src.api.rest.routes.user_routes import get_current_user_claims
# from src.config.settings import settings
# from src.utils.proxy import proxy_request

# router = APIRouter(tags=["api"])


# @router.api_route(
#     "/api",
#     methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
# )
# @router.api_route(
#     "/api/{path:path}",
#     methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
# )
# async def catch_all_api(
#     request: Request,
#     path: str = "",
#     claims: dict[str, str] = Depends(get_current_user_claims),
# ) -> Response:
#     """Proxy /api requests to the core backend after verifying the access token."""
#     url_suffix = f"/{path}" if path else ""
#     target_url = f"{settings.CORE_API_URL}/api{url_suffix}"
#     return await proxy_request(request, target_url)
