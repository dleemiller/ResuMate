"""
CoT style prompting for interview
"""
import logging
import json
from typing import Dict, List, Optional

from api.openai_api import (
    OpenAIMessages,
    OpenAIMessage,
    OpenAIRole,
    ChatCompletionFunction,
)
from api.openai_api import GPT35Turbo as GPTApi
from cache.vectordb import ResponseCache, RecruiterResponse, CacheList
from tasks.dot_logger import DotLogger
from tasks.models.recruiter import InterviewStep, Audience


system_prompt = """
As a skilled technical recruiter, your task is to evaluate a candidate for a specific role in the [specify industry, e.g., software development, IT management]. The evaluation includes a thorough resume review and a detailed interview, followed by writing a recommendation letter.

Phase 1: Resume Review
- Identify and summarize key qualifications and relevant experiences from the resume.
- Use chain-of-thought reasoning to assess how these experiences align with the job requirements.
- Consider the impact of missing skills or experiences on the candidate's suitability for the role.
- Ask a targeted question to the candidate to gain information for your recommendation letter.

Phase 2: Interview
- Conduct a focused interview to delve into the candidate's professional achievements and the practical application of their skills in previous roles.
- Ask specific questions about their past projects, challenges faced, and their contributions to these situations.
- Use chain-of-thought to analyze the candidate's responses, focusing on how their past experiences demonstrate their ability to handle the job's responsibilities.

Phase 3: Recommendation Letter
- Based on the interview and resume analysis, write a concise letter of recommendation.
- Articulate, through a reasoned approach, why the candidate's real-world experiences make them suitable for the role.

Guidelines:
- Prioritize real-world experiences and achievements in your assessment.
- Maintain a structured approach, using chain-of-thought reasoning for clarity and depth in your evaluation.
- You will have limited time with the candidate. Prioritize assessing if the candidate is broadly aligned with the position before delving into specific details.
- Do not ask questions that are adequately answered by the candidate's resume.
- Do not message the hiring manager until you are finished interviewing and have no further questions for the candidate.
- Reference the following job listing for this assessment:
  {content}
"""

assistant_prompt = """
# Thought (Phase {phase})
{thought}

# Requirement
{requirement}

# Message to {audience}
{message}
"""


class RecruitActionFunction(ChatCompletionFunction):
    name = "recruiter_action"
    description = "Next step of interview assessment."
    param_model = InterviewStep
    gpt_model = GPTApi


class Recruiter:
    function = RecruitActionFunction
    temperature = 1
    cache = ResponseCache.new()

    _system_prompt = OpenAIMessage(
        role=OpenAIRole.system,
        content=system_prompt,
    )

    _user_prompt = OpenAIMessage(
        role=OpenAIRole.user,
        name="candidate",
        content="{content}",
    )

    _assistant = OpenAIMessage(
        role=OpenAIRole.assistant,
        content=assistant_prompt,
    )

    @classmethod
    def assistant_response_to_message(cls, response) -> OpenAIMessage:
        return cls._assistant.format(
            thought=response.think_out_loud,
            requirement=response.job_requirement,
            phase=response.phase,
            audience=response.audience.value,
            message=response.message,
        )

    @classmethod
    def run(cls, job: str, resume: str, *args) -> List[Dict[str, str]]:
        messages = [
            cls._system_prompt.format(content=job),
            cls._user_prompt.format(
                content=f"Here is my resume, send me a question in your message to me:\n{resume}"
            ),
        ]

        # set the vectordb collection
        cls.cache.set_cache(CacheList.recruiter)

        while True:
            response = cls.function.call(messages, temperature=cls.temperature)
            assistant_msg = cls.assistant_response_to_message(response)
            print(assistant_msg.content)
            messages.append(assistant_msg)

            # check if exiting
            if response.audience == Audience.hiring_manager:
                return messages[1:]  # drop system message
            else:
                if response.message.strip() == "":  # prompt for question if none asked
                    user_input = "Was there a question you wanted to ask me?"
                    print(user_input)
                else:
                    # check for cached response
                    cached_response = cls.cache.threshold_query(response.message)
                    if isinstance(cached_response, str) and cached_response:
                        print(f"CACHE HIT! {cached_response}")
                        user_input = cached_response
                    else:
                        user_input = input(response.message)
                        r = RecruiterResponse(
                            question=response.message, answer=user_input
                        )
                        cls.cache.cache_question(r)

                candidate_msg = cls._user_prompt.format(content=user_input)
                messages.append(candidate_msg)
