from typing import List, ClassVar
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.exceptions import AppError
from app.core.logger import get_logger

logger = get_logger(__name__)

class JobRequest(BaseModel):
    job_title: str = Field(..., min_length=5,
                           max_length=50, str_strip_whitespace=True)
    country: str = Field(..., min_length=2, max_length=30,
                         str_strip_whitespace=True)

    # Use ClassVar for data that shouldn't be part of the API request body
    FORBIDDEN_WORDS: ClassVar[set[str]] = {
        "test", "dummy", "sample", "example", "fake", "abc"}

    @field_validator('job_title')
    @classmethod
    def validate_job_title(cls, value: str) -> str:
        words = set(value.lower().split())
        # isdisjoint => compare between two group
        if not words.isdisjoint(cls.FORBIDDEN_WORDS):
            raise AppError(f"Job title contains forbidden words.",status_code=422)
        return value

    @field_validator('country')
    @classmethod
    def validate_country(cls, value: str) -> str:
        # allow spaces
        if not all(char.isalpha() or char.isspace() for char in value):
            raise AppError(
                "Country must contain only alphabetic characters.",status_code=422)
        return value

class Skill(BaseModel):
    name: str
    count: int


class JobResponse(BaseModel):
    job_title: str
    country: str
    skills: List[Skill]
    nice_to_have: List[str]
    cities: List[str]
    experience_level: str
    advice: str


# Block unknown fields
model_config = ConfigDict(extra='forbid')
