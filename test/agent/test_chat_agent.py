import os

from camel.agent import ChatAgent
from camel.configs import ChatGPTConfig
from camel.generator import SystemMessageGenerator
from camel.message import ChatMessage
from camel.typing import ModeType, RoleType

assert os.environ.get("OPENAI_API_KEY") is not None, "Missing OPENAI_API_KEY"


def test_chat_agent():
    chat_gpt_args = ChatGPTConfig()
    system_message = SystemMessageGenerator(with_task=False).from_role(
        "doctor", RoleType.ASSISTANT)
    assistant = ChatAgent(
        system_message,
        ModeType.GPT_3_5_TURBO,
        chat_gpt_args,
    )

    assert str(assistant) == ("ChatAgent({'role_name': 'doctor'}, "
                              "RoleType.ASSISTANT, ModeType.GPT_3_5_TURBO)")

    assistant.reset()
    user_msg = ChatMessage(dict(role_name="patient"), RoleType.USER, "user",
                           "Hello!")
    messages, terminated, info = assistant.step(user_msg)

    assert terminated is False
    assert messages != []
    assert info['id'] is not None

    assistant.reset()
    user_msg = ChatMessage(dict(role_name="patient"), RoleType.USER, "user",
                           "Hello!" * 4096)
    messages, terminated, info = assistant.step(user_msg)

    assert terminated is True
    assert messages == []
    assert info['finish_reasons'][0] == "max_tokens_exceeded"
