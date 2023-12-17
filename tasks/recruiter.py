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
from tasks.dot_logger import DotLogger
from tasks.models.recruiter import InterviewStep, Audience


class RecruitActionFunction(ChatCompletionFunction):
    name = "recruiter_action"
    description = "Next step of interview assessment."
    param_model = InterviewStep
    gpt_model = GPTApi


class Recruiter:
    function = RecruitActionFunction
    temperature = 1

    _system_prompt = OpenAIMessage(
        role=OpenAIRole.system,
        content="""
As a skilled technical recruiter, your task is to evaluate a candidate for a specific role in the [specify industry, e.g., software development, IT management]. The evaluation includes a thorough resume review and a detailed interview, followed by writing a recommendation letter.

Phase 1: Resume Review
- Identify and summarize key qualifications and relevant experiences from the resume.
- Use chain-of-thought reasoning to assess how these experiences align with the job requirements.
- Consider the impact of missing skills or experiences on the candidate's suitability for the role, focusing on real scenarios.

Phase 2: Interview
- Conduct a focused interview to delve into the candidate's professional achievements and the practical application of their skills in previous roles.
- Ask specific questions about their past projects, challenges faced, and their contributions to these situations.
- Use chain-of-thought to analyze the candidate's responses, focusing on how their past experiences demonstrate their ability to handle the job's responsibilities.

Phase 3: Recommendation Letter
- Based on the interview and resume analysis, write a concise letter of recommendation.
- Articulate, through a reasoned approach, why the candidate's real-world experiences make them suitable for the role.
- Limit the letter to 300 words, ensuring it's focused and to the point.

Guidelines:
- Prioritize real-world experiences and achievements in your assessment.
- Maintain a structured approach, using chain-of-thought reasoning for clarity and depth in your evaluation.
- The task concludes with the submission of the recommendation letter to the hiring manager.
- Reference the following job listing for this assessment:
  {content}
        """,
    )

    _user_prompt = OpenAIMessage(
        role=OpenAIRole.user,
        content="""
        {content}
        """,
    )

    _assistant = OpenAIMessage(
        role=OpenAIRole.assistant,
        content="""
# Thought
{thought}

# Next Action
{next_action}

# Reasoning
{reasoning}

# Message to {audience}
{message}
        """,
    )

    @classmethod
    def run(cls, job: str, resume: str, *args) -> List[Dict[str, str]]:
        messages = [
            cls._system_prompt.format(content=job),
            cls._user_prompt.format(
                content=f"Here is my resume, ask me a question:\n{resume}"
            ),
        ]

        while True:
            response = cls.function.call(messages, temperature=cls.temperature)
            if response.audience == Audience.hiring_manager:
                return messages[1:]  # drop system message
            else:
                assistant_msg = cls._assistant.format(
                    thought=response.think_out_loud,
                    next_action=response.next_action,
                    reasoning=response.job_requirement_reasoning,
                    audience=response.audience.value,
                    message=response.message,
                )

                print(assistant_msg.content)

                # check for cached response
                cached_response = None
                if isinstance(cached_response, str) and cached_response:
                    user_input = cached_response
                else:
                    user_input = input(response.message)
                candidate_msg = cls._user_prompt.format(content=user_input)
                messages += [assistant_msg, candidate_msg]
