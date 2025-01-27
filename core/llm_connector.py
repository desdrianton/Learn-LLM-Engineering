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
    _context = []

    def __init__(self, model):
        self._model = model

    def _push_context(self, *, system_prompt=None, user_prompt=None, assistant_result=None) -> list:
        if system_prompt is not None:
            self._context.append({"role": "system", "content": system_prompt})
        if user_prompt is not None:
            self._context.append({"role": "user", "content": user_prompt})
        if assistant_result is not None:
            self._context.append({"role": "assistant", "content": assistant_result})

        return self._context

    def ask(self, *, system_prompt: str, user_prompt: str, **kwargs):
        pass

    def ask_with_stream_result(self, *, system_prompt: str, user_prompt: str, **kwargs):
        return self.ask(system_prompt=system_prompt, user_prompt=user_prompt, **kwargs)

    def get_context(self) -> list:
        return self._context


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

    def ask(self, *, system_prompt: str, user_prompt: str, **kwargs):
        self._push_context(system_prompt=system_prompt, user_prompt=user_prompt)

        response_format_type = None
        if kwargs is not None and kwargs.get("kwargs") is not None and kwargs.get("kwargs").get("response_format_type") is not None:
            response_format_type = kwargs.get("kwargs").get("response_format_type")

        if response_format_type is None:
            response = self._openai.chat.completions.create(
                model=self._model,
                messages=self._context
            )
        else:
            response = self._openai.chat.completions.create(
                model=self._model,
                messages=self._context,
                response_format={"type": response_format_type}
            )

        result = response.choices[0].message.content
        self._push_context(assistant_result=result)
        return result

    def ask_with_stream_result(self, *, system_prompt: str, user_prompt: str, **kwargs):
        self._push_context(system_prompt=system_prompt, user_prompt=user_prompt)
        response_format_type = None
        if kwargs is not None and kwargs.get("kwargs") is not None and kwargs.get("kwargs").get("response_format_type") is not None:
            response_format_type = kwargs.get("kwargs").get("response_format_type")

        if response_format_type is None:
            response = self._openai.chat.completions.create(
                model=self._model,
                messages=self._context,
                stream=True
            )
        else:
            response = self._openai.chat.completions.create(
                model=self._model,
                messages=self._context,
                response_format={"type": response_format_type},
                stream=True
            )

        return response


# ======================================================================================================================
# OllamaConnector
# ======================================================================================================================
class OllamaConnector(LLMConnector):
    MODEL_llama3_2: str = "llama3.2"

    def __init__(self, model: str = MODEL_llama3_2):
        super().__init__(model=model)

    def ask(self, *, system_prompt: str, user_prompt: str, **kwargs):
        self._push_context(system_prompt=system_prompt, user_prompt=user_prompt)
        response = ollama.chat(model=self._model, messages=self._context)

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

    def ask(self, *, system_prompt: str, user_prompt: str, **kwargs):
        self._push_context(system_prompt=system_prompt, user_prompt=user_prompt)

        response = self._claude.messages.create(
            model=self._model,
            system=system_prompt,
            max_tokens=8192,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )

        result = response.content[0].text
        self._push_context(assistant_result=result)
        return result

    def ask_with_stream_result(self, *, system_prompt: str, user_prompt: str, **kwargs):
        self._push_context(system_prompt=system_prompt, user_prompt=user_prompt)

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

    def ask(self, *, system_prompt: str, user_prompt: str, **kwargs):
        self._push_context(system_prompt=system_prompt, user_prompt=user_prompt)

        gemini = genai.GenerativeModel(
            model_name=self._model,
            system_instruction=system_prompt
        )

        result = gemini.generate_content(user_prompt).text
        self._push_context(assistant_result=result)
        return result
