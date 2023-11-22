import logging
import json
from typing import Optional

from api.openai_api import OpenAIMessages, OpenAIMessage, OpenAIRole
from api.openai_api import GPT4 as GPTApi
from tasks.dot_logger import DotLogger
from tasks.models.resume import Resume


class ParseResume:
    """
    Use LLM to parse resume into JSON.
    """

    model = GPTApi

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
    def parse(cls, content: str, logger: logging.Logger) -> Resume:
        messages = [
            cls.system_prompt.model_dump(),
            cls._user_prompt.format(content=content).model_dump(),
        ]
        logger.info(f"messages: {json.dumps(messages)}")
        with DotLogger(logger):
            response = cls.model.create(messages, functions=[cls.function])

        message = response.choices[0].message
        logger.info(message)
        skills = Resume.parse_raw(message.function_call.arguments)
        return skills
