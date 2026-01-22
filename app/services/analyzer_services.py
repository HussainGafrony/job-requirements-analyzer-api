from app.core.logger import logger
import json


class JobDataService:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.jobs = self.load_jobs()  # We upload data only once here

    def load_jobs(self):
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return ValueError("file not found")

    def filter_jobs(self, job_title: str, country: str):

        filtered_jobs = []

        for job in self.jobs:
            if (
                job["job_title"].strip().lower() == job_title.strip().lower()
                and job["country"].strip().lower() == country.strip().lower()
            ):
                filtered_jobs.append(job)

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
        sorted_skills = sorted(
            skill_counter.items(),
            key=lambda item: item[1],
            reverse=True
        )  # item[1]=> count  this mean sorted by count not names

        top_skills = []
        nice_to_have = []

        for index, (skill, count) in enumerate(sorted_skills):
            if index < 5:
                top_skills.append({"name" : skill,"count":count})
            else:
                nice_to_have.append(skill)
                
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
        raise ValueError("Currently only Germany is supported")
