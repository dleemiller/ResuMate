import logging
import json
from typing import Optional

from api.openai_api import OpenAIMessages, OpenAIMessage, OpenAIRole, GPT35Turbo

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ResumeSkill(BaseModel):
    skill: str = Field(description="A skill that may interest an employer")
    years: Optional[float] = Field(description="Number of years of experience")


class ResumeSkills(BaseModel):
    skills: list[ResumeSkill]


class ParseResumeSkills:
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
        "parameters": ResumeSkills.schema(),
    }

    @classmethod
    def parse(cls, content: str) -> ResumeSkills:
        messages = [
            cls.system_prompt.model_dump(),
            cls._user_prompt.format(content=content).model_dump(),
        ]
        logging.info(f"messages: {json.dumps(messages)}")
        response = cls.model.create(messages, functions=[cls.function])
        return response
