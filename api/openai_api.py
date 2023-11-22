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
        new_self = self.copy()
        new_self.content = new_self.content.format(**kwargs)
        return new_self

    class Config:
        use_enum_values = True


class OpenAIMessages(BaseModel):
    messages: list[OpenAIMessage]

    def append(self, item: OpenAIMessage):
        assert isinstance(item, OpenAIMessage)
        self.messages = self.messages + [item]

    def __iter__(self):
        return iter(map(lambda x: x.model_dump(), self.messages))



class GPTModel:
    # model_name = "gpt-3.5-turbo"
    # client = OpenAI()

    @classmethod
    @backoff.on_exception(backoff.expo, APIConnectionError, max_tries=3)
    def create(cls, messages: OpenAIMessages, functions: Optional[list[dict]] = None):
        kwargs = {
            "model": cls.model_name,
            "messages": list(messages),
        }
        if functions:
            kwargs["functions"] = functions
        completion = cls.client.chat.completions.create(**kwargs)
        return completion


class GPT35Turbo(GPTModel):
    model_name = "gpt-3.5-turbo"
    client = OpenAI()


class GPT4(GPTModel):
    model_name = "gpt-4"
    client = OpenAI()

if __name__ == "__main__":
    messages = OpenAIMessages(
        messages=[OpenAIMessage(role=OpenAIRole.user, content="Tell me a joke")]
    )

    completion = GPT35Turbo.create(messages)
    print(completion.choices[0].message)
