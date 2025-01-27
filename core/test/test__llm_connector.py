from core.llm_connector import *

# ======================================================================================================================
# Prepare
# ======================================================================================================================
system_prompt: str = "Engkau adalah guru sejarah yang sangat sabar. Engkau terbiasa menjelaskan sesuatu dengan sangat panjang dan lengkap"
user_prompt: str = "Jelaskan siapakah ir. Soekarno itu? mengapa dia sangat terkenal di Indonesia?"


def test_chat_gpt():
    print(f"{'\n' * 5}{'#' * 100}\n# Ask to ChatGPT\n{'#' * 100}")
    _chat_gpt = ChatGPTConnector(model=ChatGPTConnector.MODEL_gpt_4o)
    _result = _chat_gpt.ask(system_prompt=system_prompt, user_prompt=user_prompt)
    print(_result)


def test_chat_gpt_with_stream():
    print(f"{'\n' * 5}{'#' * 100}\n# Ask to ChatGPT (Stream result)\n{'#' * 100}")
    _chat_gpt = ChatGPTConnector(model=ChatGPTConnector.MODEL_gpt_4o)
    _result = _chat_gpt.ask_with_stream_result(system_prompt=system_prompt, user_prompt=user_prompt)

    for chunk in _result:
        print(chunk.choices[0].delta.content or '', end="", flush=True)


def test_claude():
    print(f"{'\n' * 5}{'#' * 100}\n# Ask to Claude\n{'#' * 100}")
    _claude = ClaudeConnector()
    _result = _claude.ask(system_prompt=system_prompt, user_prompt=user_prompt)
    print(_result)

def test_claude_with_stream():
    print(f"{'\n' * 5}{'#' * 100}\n# Ask to Claude (Stream result)\n{'#' * 100}")
    _claude = ClaudeConnector()
    _result = _claude.ask_with_stream_result(system_prompt=system_prompt, user_prompt=user_prompt)
    with _result as stream:
        for text in stream.text_stream:
                print(text, end="", flush=True)


def test_ollama():
    print(f"{'\n' * 5}{'#' * 100}\n# Ask to Ollama\n{'#' * 100}")
    _ollama = OllamaConnector()
    _result = _ollama.ask(system_prompt=system_prompt, user_prompt=user_prompt)
    print(_result)


def test_gemini():
    print(f"{'\n' * 5}{'#' * 100}\n# Ask to Gemini\n{'#' * 100}")
    _gemini = GeminiConnector()
    _result = _gemini.ask(system_prompt=system_prompt, user_prompt=user_prompt)
    print(_result)

# ======================================================================================================================
# Run
# ======================================================================================================================
test_chat_gpt()
test_chat_gpt_with_stream()
test_claude()
test_claude_with_stream()
test_ollama()
test_gemini()
