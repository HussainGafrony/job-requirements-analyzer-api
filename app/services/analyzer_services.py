from app.core.exceptions import AppError
from app.core.logger import get_logger, logger
import json

logger = get_logger(__name__)

class JobDataService:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.jobs = self.load_jobs()  # We upload data only once here

    def load_jobs(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise AppError("Data source is missing", status_code=404)
        except json.JSONDecodeError:
            raise AppError('Data source is corrupted', status_code=404)

    def filter_jobs(self, job_title: str, country: str):

        filtered_jobs = []

        for job in self.jobs:
            if (
                job["job_title"].strip().lower() == job_title.strip().lower()
                and job["country"].strip().lower() == country.strip().lower()
            ):
                filtered_jobs.append(job)
        if not filtered_jobs:
            raise AppError(
                f"No results found for '{job_title}' in '{country}'", status_code=404)

        return filtered_jobs

    def analyze_skills(self, jobs: list) -> dict:
        skill_counter = {}
        cities = set()
        levels = set()
        for job in jobs:
            if job.get("city"):
                cities.add(job["city"])
            if job.get("experience_level"):
                levels.add(job["experience_level"])
            skills = job.get("skills", [])
            if not isinstance(skills, list):
                continue
            for skill in skills:
                if isinstance(skill, str):
                    skill_counter[skill] = skill_counter.get(skill, 0)+1
                else:
                    print(
                        f"Warning: skipped invalid skill type: {type(skill)}")
                    # item[1]=> count  this mean sorted by count not names
        sorted_skills = sorted(
            skill_counter.items(),
            key=lambda item: item[1],
            reverse=True
        )

        # Slice from the start until index 5 & unpack (s,c) to create a list of dictionaries
        top_skills = [{"name": s, "count": c} for s, c in sorted_skills[:5]]
        # Slice from index 5 until the very end & unpack (s,_) and take only 's' because we don't need count (_)
        nice_to_have = [s for s, _ in sorted_skills[5:]]

        first_skill = top_skills[0]['name'] if top_skills else "python"
        advice_text = f"Focus on {first_skill} to increase your chances in this market"
        return {
            "skills": top_skills,
            "nice_to_have": nice_to_have,
            "cities": cities,
            "experience_level": ", ".join(levels) if levels else "Not specified",
            "advice": advice_text
        }


def analyze_job(job_title: str, country: str):
    logger.info(f"Analyzing job: {job_title} in {country}")

    if country.lower() != "germany":
        logger.warning(f"Unsupported country requested: {country}")
        raise AppError("Currently only Germany is supported", status_code=404)
