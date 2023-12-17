from enum import Enum
from pydantic import BaseModel, Field


class Audience(Enum):
    candidate = "candidate"
    hiring_manager = "hiring_manager"


class InterviewStep(BaseModel):
    think_out_loud: str = Field(description="identify what experience is missing from the candidate's resume")
    job_requirement: str = Field(
        description="the specific part of the job listing you want to determine experience for"
    )
    next_action: str = Field(
        description="describe your next action"
    )

    audience: Audience = Field(
        description="candidate or hiring_manager, any message to the hiring_manager will terminate the interview"
    )
    message: str = Field(
        description="one question for the candidate or your full letter of recommendation for the hiring manager"
    )
