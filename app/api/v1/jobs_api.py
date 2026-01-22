from fastapi import APIRouter, HTTPException
from app.schemas.job_schema import JobRequest, JobResponse
from app.services.analyzer_services import *

router = APIRouter(prefix="/jobs", tags=["Jobs"])

job_Data_Service = JobDataService("./app/data/jobs_data.json")

@router.post("/analyze", response_model=JobResponse,
             summary="Analyze job requirements",
             description="Analyze job requirements based on job title and country.")
def analyze(request: JobRequest):
    try:
        jobs = job_Data_Service.filter_jobs(
            job_title=request.job_title,
            country=request.country
        )

        if not jobs:
            raise HTTPException(
                status_code=404, detail="No jobs found for this title and country.")
        result = job_Data_Service.analyze_skills(jobs)
        return {
            "job_title": request.job_title,
            "country": request.country,
            # this mean Open this box, take all the keys and values ​​inside, and place them directly into this new dictionary.
            **result
        }
    except ValueError as e:
        # Logical errors (e.g., rejected inputs)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Any unexpected error
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please try again later."
        )
