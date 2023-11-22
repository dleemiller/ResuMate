from typing import Optional

from pydantic import BaseModel, Field


class Skill(BaseModel):
    skill: str = Field(description="A skill that may interest an employer")
    years: Optional[float] = Field(description="Number of years of experience")

    def __str__(self):
        years_str = "" if self.years is None else f" - {self.years} years"
        return f"{self.skill}{years_str}"


class Experience(BaseModel):
    place_of_work: str = Field(description="Place of work")
    job_title: str = Field(description="Job title")
    date_start: Optional[str] = Field(description="Starting date of job")
    date_end: Optional[str] = Field(description="Ending date of job")
    experience: list[str] = Field(description="Responsibility or accomplishment")

    def __str__(self):
        date_start = "n/a" if not self.date_start else self.date_start
        date_end = "n/a" if not self.date_end else self.date_end
        experiences = "  " + "\n  ".join(self.experience)
        return f"{self.job_title}, {self.place_of_work} (dates:{date_start} - {date_end})\n{experiences}"


class Education(BaseModel):
    school: str = Field(description="School issuing diploma")
    degree: str = Field(description="Degree awarded")
    date_from: Optional[str] = Field(description="Date started school")
    date_to: Optional[str] = Field(description="Date finished school")
    field_of_study: Optional[str] = Field(description="Field of study")
    courses: Optional[list[str]] = Field(description="Courses")

    def __str__(self):
        field_of_study = "" if self.field_of_study is None else self.field_of_study
        return f"{self.school} - {self.degree} ({field_of_study}), from: {self.date_from}, to: {self.date_to}"


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
        description="Any hobbies, volunteering, professional organizations, or certifications"
    )

    def short_version(self):
        education = "Education:\n  " + "\n  ".join(map(str, self.education))
        skills = "Skills:\n  " + "\n  ".join(map(str, self.skills))
        if self.personal is not None:
            personal = "Personal/Professional:\n  " + "\n  ".join(self.personal)
        else:
            personal = ""
        experiences = "Experience:\n " + "\n ".join(map(str, self.experiences))
        return f"Objective: {self.objective}\n{skills}\n{experiences}\n{education}\n{personal}"


## Note, this must be regenerated if the schema is changed
resume_schema = """
{
  "properties": {
    "name": { "type": "string", "description": "Applicant's name" },
    "email": { "type": "string", "description": "Applicant's email" },
    "phone": { "type": "string", "description": "Applicant's phone" },
    "objective": { "type": "string", "description": "Objective statement" },
    "experiences": {
      "description": "Responsibilities or accomplishments at a prior job.",
      "items": {
        "properties": {
          "place_of_work": { "type": "string", "description": "Place of work" },
          "job_title": { "type": "string", "description": "Job title" },
          "date_start": { "type": "string", "description": "Starting date of job" },
          "date_end": { "type": "string", "description": "Ending date of job" },
          "experience": { "type": "array", "items": { "type": "string" }, "description": "Responsibility or accomplishment" }
        },
        "required": ["place_of_work", "job_title"],
        "type": "object"
      },
      "description": "Experiences",
      "type": "array"
    },
    "education": {
      "description": "Educational history",
      "items": {
        "properties": {
          "school": { "type": "string", "description": "School issuing diploma" },
          "degree": { "type": "string", "description": "Degree awarded" },
          "date_from": { "type": "string", "description": "Date started school" },
          "date_to": { "type": "string", "description": "Date finished school" },
          "field_of_study": { "type": "string", "description": "Field of study" },
          "courses": { "type": "array", "items": { "type": "string" }, "description": "Courses" }
        },
        "required": ["school", "degree"],
        "type": "object"
      },
      "description": "Education",
      "type": "array"
    },
    "skills": {
      "description": "Any listed skill that would interest a potential employer.",
      "items": {
        "properties": {
          "skill": { "type": "string", "description": "A skill that may interest an employer" },
          "years": { "type": "number", "description": "Number of years of experience" }
        },
        "required": ["skill", "years"],
        "type": "object"
      },
      "description": "Skills",
      "type": "array"
    },
    "personal": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Any hobbies, volunteering, professional organizations, or certifications"
    }
  },
  "required": ["name", "email", "phone", "experiences", "education", "skills"],
  "description": "Resume",
  "type": "object"
}
"""

if __name__ == "__main__":
    # with open("test_resume.json", "r") as fh:
    #     import json

    #     resume = json.load(fh)

    # print(Resume.parse_raw(resume).short_version())
    print(Resume.schema())
