from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.jobs_api import router as jobs_router
from app.core.exceptions import AppError
from app.core.logger import logger
from app.services.analyzer_services import *

app = FastAPI(title="Job Requirements Analyzer API")


@app.exception_handler(AppError)
async def global_exception_handler(request: Request, exc: AppError):

    error_details = {
        "success": False,
        "error_info": {
            "message": exc.message,
            "status": exc.status_code,
            "path": str(request.url),
            "method": request.method,
            "client": request.client.host
        }

    }

    return JSONResponse(status_code=exc.status_code, content=error_details)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    logger.info(
        f"Completed request: {request.method} {request.url.path} "
        f"Status: {response.status_code}"
    )

    return response

app.include_router(jobs_router, prefix="/api/v1")


# service = JobDataService("app/data/jobs_data.json")
# jobs = service.filter_jobs("Backend Developer", "Germany")
# result = service.analyze_skills(jobs)
# print(result)
