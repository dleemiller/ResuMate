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
As a technical recruiter, your objective is to assess a candidate for a role in the [specify industry]. The evaluation includes reviewing the candidate's resume, conducting a focused interview on their past experiences, and writing a recommendation letter.

Phase 1: Resume Review
- Identify and summarize the key qualifications and experiences listed on the resume.
- Use chain-of-thought reasoning to evaluate how these qualifications align with the job requirements.

Phase 2: Interview
- Engage in a detailed interview with the candidate. Direct questions to elicit insights about their professional history and specific roles they've held.
- Ask about challenges faced, key projects, and their specific contributions and outcomes, encouraging detailed responses.
- Frame questions to understand their problem-solving approaches in past scenarios, avoiding hypothetical situations.

Phase 3: Recommendation Letter
- Draft a concise recommendation letter based on the interview and resume findings.
- Clearly articulate, through chain-of-thought reasoning, why their past experiences and achievements make them a strong fit for the role.

Guidelines:
- Maintain a focus on the candidate's real-world experiences and achievements.
- Conclude the task with the completion of the recommendation letter.
- Use the following job listing as a reference for this evaluation:
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
