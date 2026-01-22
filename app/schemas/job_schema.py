from typing import List, ClassVar
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

class JobRequest(BaseModel):
    job_title: str = Field(..., min_length=5, max_length=50)
    country: str = Field(..., min_length=2, max_length=30)

    # Use ClassVar for data that shouldn't be part of the API request body
    FORBIDDEN_WORDS: ClassVar[set[str]] = {"test", "dummy", "sample", "example", "fake", "abc"}

    @field_validator('job_title')
    @classmethod
    def validate_job_title(cls, value: str) -> str:
        # Clean the input and check case-insensitively
        clean_value = value.strip().lower()
        if any(word in clean_value for word in cls.FORBIDDEN_WORDS):
            raise ValueError(f"Job title contains forbidden words.")
        return value

    @field_validator('country')
    @classmethod
    def validate_country(cls, value: str) -> str:
        # Strip whitespace and check if it's alphabetic
        stripped_value = value.strip()
        # Check if contains only letters and spaces
        if not stripped_value.replace(" ", "").isalpha():
            raise ValueError("Country must contain only alphabetic characters.")
            
        return stripped_value

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


