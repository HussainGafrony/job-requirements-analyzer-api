# Job Requirements Analyzer API

A backend API built with FastAPI that analyzes job requirements for specific roles in Germany.
It provides structured insights such as required skills, experience level, and recommended learning focus.

## Features
- Job requirements analysis
- Strong request validation
- Clean architecture
- Professional error handling
- Request logging (middleware-based)

## Tech Stack
- Python 3
- FastAPI
- Pydantic
- Uvicorn

## Project Structure
app/
├── api/
├── data/
├── schemas/
├── services/
└── main.py


## Run Locally
```bash
python -m venv venv
venv\Scripts\activate
python -m pip install fastapi uvicorn
python -m uvicorn app.main:app --reload

POST /api/v1/jobs/analyze

# Example Request
{
  "job_title": "Backend Developer",
  "country": "Germany"
}

# Example Response
{
  "job_title": "Backend Developer",
  "country": "Germany",
  "skills": [
    {
      "name": "Java",
      "priority": 1,
      "reason": "Most common requirement"
    }
  ],
  "experience_level": "Entry"
}

Notes

Currently, only Germany is supported.