from typing import Optional

from pydantic import BaseModel, Field
from tasks.models.function_call import convert_pydantic_to_openai_tool


class Skill(BaseModel):
    skill: str = Field(description="A skill that may interest an employer")
    years: Optional[float] = Field(
        description="Number of years of experience", default=None
    )

    def __str__(self):
        years_str = "" if self.years is None else f" - {self.years} years"
        return f"{self.skill}{years_str}"


class Experience(BaseModel):
    place_of_work: str = Field(description="Place of work")
    job_title: str = Field(description="Job title")
    date_start: Optional[str] = Field(description="Starting date of job", default=None)
    date_end: Optional[str] = Field(description="Ending date of job", default=None)
    experience: list[str] = Field(
        description="Responsibility or accomplishment", default=[]
    )

    def __str__(self):
        date_start = "n/a" if not self.date_start else self.date_start
        date_end = "n/a" if not self.date_end else self.date_end
        experiences = "  " + "\n  ".join(self.experience)
        return f"{self.job_title}, {self.place_of_work} (dates:{date_start} - {date_end})\n{experiences}"


class Education(BaseModel):
    school: str = Field(description="School issuing diploma")
    degree: Optional[str] = Field(description="Degree awarded", default=None)
    date_from: Optional[str] = Field(description="Date started school", default=None)
    date_to: Optional[str] = Field(description="Date finished school", default=None)
    field_of_study: Optional[str] = Field(description="Field of study", default=None)
    courses: list[str] = Field(description="Courses", default=[])

    def __str__(self):
        field_of_study = "" if self.field_of_study is None else self.field_of_study
        return f"{self.school} - {self.degree} ({field_of_study}), from: {self.date_from}, to: {self.date_to}"


class Resume(BaseModel):
    name: str = Field(description="Applicant's name")
    email: Optional[str] = Field(description="Applicant's email", default=None)
    phone: Optional[str] = Field(description="Applicant's phone", default=None)
    objective: Optional[str] = Field(
        description="Objective statement or summary of skills",
        default=None,
    )
    experiences: list[Experience] = Field(
        description="Responsibilities or accomplishments at a prior job.",
        default=[],
    )
    education: list[Education] = Field(description="Educational history", default=[])
    skills: list[Skill] = Field(
        description="Any listed skill that would interest a potential employer.",
        default=[],
    )
    personal: list[str] = Field(
        description="Any hobbies, volunteering, professional organizations, or certifications",
        default=[],
    )

    @classmethod
    def function_call(cls, function_name, function_description):
        return convert_pydantic_to_openai_tool(cls, function_name, function_description)

    def short_version(self):
        education = "Education:\n  " + "\n  ".join(map(str, self.education))
        skills = "Skills:\n  " + "\n  ".join(map(str, self.skills))
        if self.personal is not None:
            personal = "Personal/Professional:\n  " + "\n  ".join(self.personal)
        else:
            personal = ""
        experiences = "Experience:\n " + "\n ".join(map(str, self.experiences))
        return f"Objective: {self.objective}\n{skills}\n{experiences}\n{education}\n{personal}"


if __name__ == "__main__":
    # with open("test_resume.json", "r") as fh:
    #     import json

    #     resume = json.load(fh)

    # print(Resume.parse_raw(resume).short_version())
    print(Resume.schema())
