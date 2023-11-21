import logging
import json
from typing import Optional

from api.openai_api import OpenAIMessages, OpenAIMessage, OpenAIRole, GPT35Turbo

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Skill(BaseModel):
    described: str = Field(
        description="Briefly describe what the skill is and who uses it."
    )
    skill: str = Field(description="A skill that may interest an employer")
    years: Optional[float] = Field(description="Number of years of experience")


class Experience(BaseModel):
    place_of_work: str = Field(description="Place of work")
    date_start: Optional[str] = Field(description="Starting date of job")
    date_end: Optional[str] = Field(description="Ending date of job")
    job_title: str = Field(description="Job title")
    experience: list[str] = Field(description="Responsibility or accomplishment")


class Education(BaseModel):
    school: str = Field(description="School issuing diploma")
    degree: str = Field(description="Degree awarded")
    date_from: Optional[str] = Field(description="Date started school")
    date_to: Optional[str] = Field(description="Date finished school")
    field_of_study: Optional[str] = Field(description="Field of study")
    courses: Optional[list[str]] = Field(description="Courses")


class Resume(BaseModel):
    name: Optional[str] = Field(description="Applicant's name")
    email: Optional[str] = Field(description="Applicant's email")
    phone: Optional[str] = Field(description="Applicant's phone")
    objective: Optional[str] = Field(description="Objective statement")
    experiences: list[Experience] = Field(
        description="Responsibilities or accomplishments at a prior job."
    )
    education: list[Education] = Field(description="Educational history")
    skills: list[Skill] = Field(
        description="Any listed skill that would interest a potential employer."
    )
    personal: Optional[list[str]] = Field(
        description="Any hobbies, volunteering, professional organizations, etc"
    )


class ParseResume:
    """
    Use LLM to parse resume into JSON.
    """

    model = GPT35Turbo

    system_prompt = OpenAIMessage(
        role=OpenAIRole.system,
        content="""You will be given an applicant's resume. As an expert recruiter, your task is
        to identify all job skills listed or demonstrated in the document. Carefully evaluate the text
        and extract any information that might interest a potential employer.
        """,
    )

    _user_prompt = OpenAIMessage(
        role=OpenAIRole.user,
        content="""Here is the resume to use for this task:
        {content}
        """,
    )

    function = {
        "name": "write_skills",
        "description": "Writes the list of skills.",
        "parameters": Resume.schema(),
    }

    @classmethod
    def parse(cls, content: str) -> Resume:
        messages = [
            cls.system_prompt.model_dump(),
            cls._user_prompt.format(content=content).model_dump(),
        ]
        logging.info(f"messages: {json.dumps(messages)}")
        response = cls.model.create(messages, functions=[cls.function])

        message = response.choices[0].message
        logger.info(message)
        skills = Resume.parse_raw(message.function_call.arguments)
        return skills
