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
from api.openai_api import GPT41106Preview as GPTApi
from cache.vectordb import ResponseCache, RecruiterResponse, CacheList
from tasks.dot_logger import DotLogger
from tasks.models.recruiter import InterviewStep, Audience


system_prompt = """
As a technical recruiter, evaluate a candidate for {job_listing}.

Phase 1: Job/Resume Review
- Exhaustively contrast each requirement for position with skills and experiences in the resume. Write your thoughts step by step. This is the initial phase and forms the basis for the interview questions.
- Identify and ask your first question, based on the largest disparity you identify between the position and the resume.

Phase 2: Interview
- After completing the review, ask interview questions based on insights gained. Dynamically adapt the questions based on previous answers, ensuring to explore different areas of the job listing.
- Aim to cover all job aspects, ensuring a comprehensive understanding of the candidate's capabilities. Avoid repetitive questioning; move to new topics within 2 questions.
- Use chain of thought reasoning to determine the optimal question for obtaining novel information about the candidate.
- Message your question to the candidate.

Phase 3: Recommendation
- Summarize your findings in a message to the hiring manager. This phase concludes the interview process.
- The recommendation should reflect a comprehensive assessment, outlining all details for how the candidate connects to each requirement.

Guidelines:
- Follow the phase order strictly: 1 -> 2 -> 3 (finished)
- Ensure each phase is fully addressed before moving to the next.
- Conclude the interview only after all job requirements have been explored and understood.
- Maintain clear and effective communication throughout the interview process.
"""

assistant_prompt = """
# Chain of Thought (Phase {phase})
{thought}

# Job Requirement
{requirement}

# Question Brainstorming
{brainstorm}

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
            brainstorm=response.brainstorm,
        )

    @classmethod
    def run(cls, job: str, resume: str, *args) -> List[Dict[str, str]]:
        messages = [
            cls._system_prompt.format(job_listing=job),
            cls._user_prompt.format(
                content=f"Here is my resume:\n{resume}.\n\nPhase 1: begin"
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
