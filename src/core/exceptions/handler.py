"""Exception handlers for FastAPI application."""

from typing import cast

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from src.core.exceptions.base_exception import GatewayException


async def gateway_exception_handler(
    request: Request, exc: GatewayException
) -> JSONResponse:
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_type": exc.__class__.__name__,
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error_type": "InternalServerError",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        GatewayException,
        cast(ExceptionHandler, gateway_exception_handler),
    )
    app.add_exception_handler(
        Exception,
        cast(ExceptionHandler, general_exception_handler),
    )
