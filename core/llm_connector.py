from os import getenv

import ollama
from dotenv import load_dotenv
from openai import OpenAI


# ======================================================================================================================
# LLMConnector
# ======================================================================================================================
class LLMConnector:
    @staticmethod
    def _generate_message(*, system_prompt, user_prompt) -> list:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        pass


# ======================================================================================================================
# ChatGPTConnector
# ======================================================================================================================
class ChatGPTConnector(LLMConnector):
    _openai: OpenAI

    def __init__(self):
        super().__init__()
        load_dotenv()
        getenv('OPENAI_API_KEY')
        self._openai = OpenAI()

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        response_format_type = None
        if kwargs is not None and kwargs.get("kwargs") is not None and kwargs.get("kwargs").get("response_format_type") is not None:
            response_format_type = kwargs.get("kwargs").get("response_format_type")

        if response_format_type is None:
            response = self._openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt)
            )
        else:
            response = self._openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt),
                response_format={"type": response_format_type}
            )

        return response.choices[0].message.content


# ======================================================================================================================
# OllamaConnector
# ======================================================================================================================
class OllamaConnector(LLMConnector):
    MODEL: str = "llama3.2"

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        response = ollama.chat(model=self.MODEL, messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt))

        return response['message']['content']
