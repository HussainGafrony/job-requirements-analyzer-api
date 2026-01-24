from fastapi import FastAPI
from app.api.v1.jobs_api import router as jobs_router
from app.core.exceptions import *
from app.core.logger import get_logger
from app.services.analyzer_services import *
from contextlib import asynccontextmanager

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Job Analyzer API...")
    yield
    logger.info("Shutting down Job Analyzer API...")

app = FastAPI(title="Job Requirements Analyzer API", lifespan=lifespan)
# App Error
app.add_exception_handler(AppError, universal_exception_handler)
# Schema/Validation
app.add_exception_handler(RequestValidationError, universal_exception_handler)
# System Error
app.add_exception_handler(Exception, universal_exception_handler)
#router
app.include_router(jobs_router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message:":"Welcome to Job Requirements Analyzer API"}

