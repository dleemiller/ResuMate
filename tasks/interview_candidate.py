import logging
import json
from typing import Optional

from api.openai_api import OpenAIMessages, OpenAIMessage, OpenAIRole, GPT35Turbo

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class InterviewCandidate:
    """
    Use LLM to perform interview screening.
    """

    model = GPT35Turbo

    _system_prompt = OpenAIMessage(
        role=OpenAIRole.system,
        content="""Your are an expert interviewer. You will be given a job listing.
        Your task is to ask questions for the candidate to answer and try to determine if they are
        a good fit for the position. Be sure to probe deeper and deeper with your questions. If
        the candidate does not have the direct experience you are looking for, ask questions to determine
        if they have similar skills or experiences that might be applicable.

        This should be conversational. You job is to ask tough questions and challenge the applicant in order
        to get the most accurate representation of their capabilities.

        Here is the job listing to use for this task:
        {job_listing}

        Start by asking one question of the candidate.
        """,
    )

    _user_prompt = OpenAIMessage(
        role=OpenAIRole.user,
        content="{answer}",
    )

    _assistant_prompt = OpenAIMessage(
        role=OpenAIRole.assistant,
        content="{question}",
    )

    @classmethod
    def interview(cls, job_listing: str):
        messages, question = cls.begin_interview(job_listing)
        while True:
            answer = str(input(question))
            if answer.lower() == "exit":
                break
            messages, question = cls.interact(messages, answer)

        with open("interview.json", "w") as fh:
            json.dump(messages.model_dump(), fh, indent=4)

        logger.info("Successful interview.")

    @classmethod
    def begin_interview(cls, job_listing) -> tuple[OpenAIMessages, str]:
        messages = OpenAIMessages(
            messages=[
                cls._system_prompt.format(job_listing=job_listing),
                cls._user_prompt.format(
                    answer="I am ready to begin. Ask me a question."
                ).model_dump(),
            ]
        )
        logging.debug(f"messages: {list(messages)}")
        response = cls.model.create(messages)

        question = response.choices[0].message.content
        messages.append(cls._assistant_prompt.format(question=question))
        logger.info(question)
        return messages, question

    @classmethod
    def interact(cls, messages, answer: str) -> tuple[list[dict], str]:
        messages.append(cls._user_prompt.format(answer=answer))
        logging.debug(f"messages: {list(messages)}")
        response = cls.model.create(messages)

        question = response.choices[0].message.content
        logger.info(question)
        messages.append(cls._assistant_prompt.format(question=question))
        return messages, question
