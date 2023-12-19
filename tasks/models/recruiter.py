from enum import Enum
from pydantic import BaseModel, Field


class Audience(Enum):
    candidate = "candidate"
    hiring_manager = "hiring_manager"


class InterviewStep(BaseModel):
    phase: int = Field(
        description="Indicate the current phase: 1 for Job/Resume Review, 2 for Interview, 3 for Recommendation."
    )
    think_out_loud: str = Field(
        description="Use chain of thought to determine which job requirements have and have not been addressed. Guide the next question based on this reflection."
    )
    job_requirement: str = Field(
        description="Define the specific skill or experience from the job listing to explore next."
    )
    brainstorm: str = Field(
        description="Critically reason what your next message should contain by drawing on the requirements and candidate information."
    )
    audience: Audience = Field(
        description="Choose 'candidate' to continue the interview, 'hiring_manager' to conclude and summarize."
    )
    message: str = Field(
        description="Compose a question for the candidate, or summarize findings for the hiring manager."
    )
