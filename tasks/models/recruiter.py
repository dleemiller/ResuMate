from enum import Enum
from pydantic import BaseModel, Field


class Audience(Enum):
    candidate = "candidate"
    hiring_manager = "hiring_manager"


class InterviewStep(BaseModel):
    think_out_loud: str = Field(description="identify what is missing from the resume")
    next_action: str = Field(
        description="description of what you need to accomplish next"
    )
    job_requirement_reasoning: str = Field(
        description="the part of the job listing this will elucidate and how"
    )
    audience: Audience = Field(
        description="candidate or hiring_manager, any message to the hiring_manager will terminate the interview"
    )
    message: str = Field(
        description="one question for the candidate or your full letter of recommendation for the hiring manager"
    )
