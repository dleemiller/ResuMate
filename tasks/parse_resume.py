import logging
import json
from typing import Optional

from api.openai_api import OpenAIMessages, OpenAIMessage, OpenAIRole
from api.openai_api import GPT35Turbo as GPTApi
from tasks.dot_logger import DotLogger
from tasks.models.resume import Resume


class ParseResume:
    """
    Use LLM to parse resume into JSON.
    """

    model = GPTApi
    temperature = 0.1

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

    function = Resume.function_call(
        function_name="write_skills",
        function_description="Writes the list of skills and experiences.",
    )

    @classmethod
    def parse(cls, content: str, logger: logging.Logger) -> Resume:
        messages = [
            cls.system_prompt.dict(),
            cls._user_prompt.format(content=content).dict(),
        ]
        logger.info(f"messages: {json.dumps(messages, indent=4)}")
        with DotLogger(logger):
            response = cls.model.create(
                messages, function=cls.function, temperature=cls.temperature
            )

        message = response.choices[0].message
        logger.info(message)
        resume = Resume.parse_raw(message.tool_calls[0].function.arguments)
        return resume
