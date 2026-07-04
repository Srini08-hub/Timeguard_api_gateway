from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from src.api.middleware.cors import setup_cors
from src.api.rest.routes.assignment_routes import router as assignment_router

# from src.api.rest.routes.api_routes import router as api_router
from src.api.rest.routes.attachment_routes import router as attachment_router
from src.api.rest.routes.auth_routes import router as auth_router
from src.api.rest.routes.client_routes import router as client_router
from src.api.rest.routes.client_rule_routes import router as client_rule_router
from src.api.rest.routes.content_extract_routes import router as content_extract_router
from src.api.rest.routes.department_routes import router as department_router
from src.api.rest.routes.email_routes import router as email_router
from src.api.rest.routes.employee_routes import router as employee_router
from src.api.rest.routes.polling_routes import router as polling_router
from src.api.rest.routes.timecard_routes import router as timecard_router
from src.api.rest.routes.timesheet_routes import router as timesheet_router
from src.api.rest.routes.user_routes import router as user_router
from src.config.settings import settings
from src.core.exceptions import handler as exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan event to manage pooled HTTPX AsyncClient lifecycle."""
    limits = httpx.Limits(
        max_connections=settings.HTTP_CLIENT_MAX_CONNECTIONS,
        max_keepalive_connections=settings.HTTP_CLIENT_MAX_KEEPALIVE_CONNECTIONS,
    )
    app.state.http_client = httpx.AsyncClient(
        timeout=settings.HTTP_CLIENT_TIMEOUT,
        limits=limits,
    )
    yield
    await app.state.http_client.aclose()


def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    setup_cors(app)

    # Register gateway routers
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(email_router)
    app.include_router(timesheet_router)
    app.include_router(timecard_router)
    app.include_router(employee_router)
    app.include_router(client_router)
    app.include_router(client_rule_router)
    app.include_router(department_router)
    app.include_router(assignment_router)
    app.include_router(content_extract_router)
    app.include_router(attachment_router)
    app.include_router(polling_router)
    # app.include_router(api_router)

    # Register exception handlers
    exception_handlers.register_exception_handlers(app)
    return app
