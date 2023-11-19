import backoff
from enum import Enum

from openai import OpenAI, APIConnectionError
from pydantic import BaseModel


class OpenAIRole(str, Enum):
    assistant = "assistant"
    system = "system"
    user = "user"

class OpenAIMessage(BaseModel):
    role: OpenAIRole
    content: str

class OpenAIMessages(BaseModel):
    messages: list[OpenAIMessage]

    def __iter__(self):
        return iter(self.messages)

class GPT35Turbo:
    model_name = "gpt-3.5-turbo"
    client = OpenAI()

    @classmethod
    @backoff.on_exception(backoff.expo, APIConnectionError, max_tries=3)
    def create(cls, messages: OpenAIMessages):
        completion = cls.client.chat.completions.create(
            model=cls.model_name,
            messages=list(messages)
        )
        return completion


if __name__ == "__main__":
    messages = OpenAIMessages(messages=[
        OpenAIMessage(
            role=OpenAIRole.user,
            content="Tell me a joke"
        )
    ])

    completion = GPT35Turbo.create(messages)
    print(completion.choices[0].message)
