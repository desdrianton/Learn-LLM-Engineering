from os import getenv
from dotenv import load_dotenv
from ollama import chat
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

    def ask(self, *, system_prompt, user_prompt):
        pass


# ======================================================================================================================
# ChatGPTConnector
# ======================================================================================================================
class ChatGPTConnector(LLMConnector):
    _openai: OpenAI = None

    def __init__(self):
        super().__init__()
        load_dotenv()
        getenv('OPENAI_API_KEY')
        self._openai = OpenAI()

    def ask(self, *, system_prompt, user_prompt):
        response = self._openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt)
        )

        return response.choices[0].message.content


# ======================================================================================================================
# OllamaConnector
# ======================================================================================================================
class OllamaConnector(LLMConnector):
    MODEL: str = "llama3.2"

    def ask(self, *, system_prompt, user_prompt):
        response = chat(model=self.MODEL, messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt))

        return response['message']['content']
