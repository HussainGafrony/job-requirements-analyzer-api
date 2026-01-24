from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger


class AppError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


async def universal_exception_handler(request: Request, exc: Exception):
    # 1_ Default Values (for unknown system errors)
    status_code = 500
    message = "An internal server error occurred"
    error_type = "SystemError"
    # 2_ Check it's your CUSTOM error (AppError)
    if isinstance(exc, AppError):
        status_code = exc.status_code
        message = exc.message
        error_type = "AppError"
        logger.error(
            f"{error_type} | Path: {request.url.path} | Message: {message}")
    # 3_Check if it's a SCHEMA error (RequestValidationError)
    elif isinstance(exc, RequestValidationError):
        status_code = 422
        message = "Invalid data format.",
        error_type = "ValidationError",
        logger.error(
            f"{error_type} | Path: {request.url.path} | Details: {exc.errors()}")
    # 4. It's an UNEXPECTED crash
    else:
        logger.critical(
            f"System Crash | Path: {request.url.path} | Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error_info": {
                "type": error_type,
                "message": message,
                "path": str(request.url),
                "method": request.method
            }
        }
    )
