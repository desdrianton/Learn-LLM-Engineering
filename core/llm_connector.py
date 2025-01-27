from os import getenv

import ollama
from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

# ======================================================================================================================
# LLMConnector
# ======================================================================================================================
class LLMConnector:
    _model: str

    def __init__(self, model):
        self._model = model

    @staticmethod
    def _generate_message(*, system_prompt, user_prompt) -> list:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        pass

    def ask_with_stream_result(self, *, system_prompt, user_prompt, **kwargs):
        return self.ask(system_prompt=system_prompt, user_prompt=user_prompt, **kwargs)


# ======================================================================================================================
# ChatGPTConnector
# ======================================================================================================================
class ChatGPTConnector(LLMConnector):
    MODEL_gpt_4o_mini: str = "gpt-4o-mini"
    MODEL_gpt_4o: str = "gpt-4o"

    _openai: OpenAI

    def __init__(self, model: str = MODEL_gpt_4o):
        super().__init__(model=model)
        load_dotenv()
        getenv('OPENAI_API_KEY')
        self._openai = OpenAI()

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        response_format_type = None
        if kwargs is not None and kwargs.get("kwargs") is not None and kwargs.get("kwargs").get("response_format_type") is not None:
            response_format_type = kwargs.get("kwargs").get("response_format_type")

        if response_format_type is None:
            response = self._openai.chat.completions.create(
                model=self._model,
                messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt)
            )
        else:
            response = self._openai.chat.completions.create(
                model=self._model,
                messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt),
                response_format={"type": response_format_type}
            )

        return response.choices[0].message.content

    def ask_with_stream_result(self, *, system_prompt, user_prompt, **kwargs):
        response_format_type = None
        if kwargs is not None and kwargs.get("kwargs") is not None and kwargs.get("kwargs").get("response_format_type") is not None:
            response_format_type = kwargs.get("kwargs").get("response_format_type")

        if response_format_type is None:
            return self._openai.chat.completions.create(
                model=self._model,
                messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt),
                stream=True
            )
        else:
            return self._openai.chat.completions.create(
                model=self._model,
                messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt),
                response_format={"type": response_format_type},
                stream=True
            )


# ======================================================================================================================
# OllamaConnector
# ======================================================================================================================
class OllamaConnector(LLMConnector):
    MODEL_llama3_2: str = "llama3.2"

    def __init__(self, model: str = MODEL_llama3_2):
        super().__init__(model=model)

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        response = ollama.chat(model=self._model,
                               messages=self._generate_message(system_prompt=system_prompt, user_prompt=user_prompt))

        return response['message']['content']


# ======================================================================================================================
# ClaudeConnector
# ======================================================================================================================
class ClaudeConnector(LLMConnector):
    MODEL_claude_3_5_sonnet_20240620: str = "claude-3-5-sonnet-20240620"
    _claude: Anthropic

    def __init__(self, model: str = MODEL_claude_3_5_sonnet_20240620):
        super().__init__(model=model)
        load_dotenv()
        getenv("ANTHROPIC_API_KEY")
        self._claude = Anthropic()

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        response = self._claude.messages.create(
            model=self._model,
            system=system_prompt,
            max_tokens=8192,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.content[0].text

    def ask_with_stream_result(self, *, system_prompt, user_prompt, **kwargs):
        return self._claude.messages.stream(
            model=self._model,
            system=system_prompt,
            max_tokens=8192,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )

# ======================================================================================================================
# GeminiConnector
# ======================================================================================================================
class GeminiConnector(LLMConnector):
    MODEL_gemini_1_5_flash: str = "gemini-1.5-flash"

    def __init__(self, model: str = MODEL_gemini_1_5_flash):
        super().__init__(model=model)
        load_dotenv()
        google_api_key = getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)

    def ask(self, *, system_prompt, user_prompt, **kwargs):
        gemini = genai.GenerativeModel(
            model_name=self._model,
            system_instruction=system_prompt
        )

        return gemini.generate_content(user_prompt).text
