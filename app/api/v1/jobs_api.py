from fastapi import APIRouter, HTTPException
from app.schemas.job_schema import JobRequest, JobResponse
from app.services.analyzer_services import *

router = APIRouter(prefix="/jobs", tags=["Jobs"])

job_Data_Service = JobDataService("./app/data/jobs_data.json")


@router.post("/analyze", response_model=JobResponse,
             summary="Analyze job requirements",
             description="Analyze job requirements based on job title and country.")
def analyze(request: JobRequest):
    jobs = job_Data_Service.filter_jobs(
        request.job_title,
        request.country
    )

    result = job_Data_Service.analyze_skills(jobs)
    return {
        "job_title": request.job_title,
        "country": request.country,
        # this mean Open this box, take all the keys and values ​​inside, and place them directly into this new dictionary.
        **result
    }
