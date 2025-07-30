from __future__ import annotations

import datetime as _dt
from typing import Any
from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.types import AppException


def _payload(request: Request, message: str, code: str, status_code: int, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {
        "timestamp": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "path": request.url.path,
        "error": {
            "code": code,
            "message": message,
            "status": status_code
        }
    }

    if extra:
        data["error"]["details"] = extra
    
    return data


def add_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            _payload(request, exc.detail, "http_error", exc.status_code),
            status_code=exc.status_code
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            _payload(
                request,
                "Validation failed",
                "validation_error",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                extra=exc.errors(),
            ),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            _payload(request, exc.message, exc.error_code, exc.status_code),
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            _payload(request, "Internal server error", "internal_error", status.HTTP_500_INTERNAL_SERVER_ERROR),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

