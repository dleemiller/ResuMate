import backoff
import logging
from enum import Enum
from typing import Optional, List, Type, Dict, Any

from openai import OpenAI, APIConnectionError
from pydantic import BaseModel
from api import function_call


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
    messages: List[OpenAIMessage]

    def append(self, item: OpenAIMessage):
        assert isinstance(item, OpenAIMessage)
        self.messages = self.messages + [item]

    def __iter__(self):
        return iter(map(lambda x: x.dict(), self.messages))


class GPTModel:
    # model_name = "gpt-3.5-turbo"
    # client = OpenAI()

    @classmethod
    @backoff.on_exception(backoff.expo, APIConnectionError, max_tries=3)
    def create(
        cls,
        messages: OpenAIMessages,
        function: Optional[dict] = None,
        temperature: float = 1.0,
    ):
        kwargs = {
            "model": cls.model_name,
            "messages": list(messages),
            "temperature": temperature,
        }
        if function:
            kwargs["tools"] = [function]
            kwargs["tool_choice"] = {
                "type": "function",
                "function": {"name": function["function"]["name"]},
            }
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


class ChatCompletionFunction:
    name: str
    description: str
    param_model: Type[BaseModel]
    gpt_model: Type[GPTModel]

    @classmethod
    def parse_function_params(cls, fn_params: Dict[str, Any]) -> Type[BaseModel]:
        return cls.param_model.parse_raw(fn_params)

    @classmethod
    def call(cls, messages: OpenAIMessages, temperature: float = 0.0) -> Type[BaseModel]:
        function = function_call.convert_pydantic_to_openai_tool(
            cls.param_model, cls.name, cls.description,
        )
        response = cls.gpt_model.create(
            cls._serialize_messages(messages), function=function, temperature=temperature,
        )
        message = response.choices[0].message
        fn_params = message.tool_calls[0].function.arguments
        return cls.parse_function_params(fn_params)
    
    @classmethod
    def _serialize_messages(cls, messages: OpenAIMessages) -> List[Dict[str, Any]]:
        return [
            m.dict() for m in messages
        ]
