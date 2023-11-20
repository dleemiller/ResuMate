import backoff
import logging
from enum import Enum
from typing import Optional

from openai import OpenAI, APIConnectionError
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class OpenAIRole(str, Enum):
    assistant = "assistant"
    system = "system"
    user = "user"


class OpenAIMessage(BaseModel):
    role: OpenAIRole
    content: str

    def format(self, **kwargs):
        self.content = self.content.format(**kwargs)
        return self

    class Config:
        use_enum_values = True


class OpenAIMessages(BaseModel):
    messages: list[OpenAIMessage]

    def __iter__(self):
        return iter(map(lambda x: x.json, self.messages))


# class GPT35TurboAssistant:
#     def __init__(self, client, assistant):
#         self.client = client
#         self.assistant = assistant
#         self.thread = client.beta.threads.create()
#
#     def create(self, message: OpenAIMessage):
#         pass


class GPT35Turbo:
    model_name = "gpt-3.5-turbo"
    client = OpenAI()

    @classmethod
    @backoff.on_exception(backoff.expo, APIConnectionError, max_tries=3)
    def create(cls, messages: OpenAIMessages, functions: Optional[list[dict]] = None):
        completion = cls.client.chat.completions.create(
            model=cls.model_name,
            messages=list(messages),
            functions=functions,
        )
        return completion


#     def __enter__(self, name: str, instructions: str):
#         assistant = client.beta.assistants.create(
#             name=name,
#             instructions=instructions,
#             model=self.model_name,
#         )


if __name__ == "__main__":
    messages = OpenAIMessages(
        messages=[OpenAIMessage(role=OpenAIRole.user, content="Tell me a joke")]
    )

    completion = GPT35Turbo.create(messages)
    print(completion.choices[0].message)
