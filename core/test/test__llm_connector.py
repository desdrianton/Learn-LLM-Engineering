from core.llm_connector import *

# ======================================================================================================================
# Prepare
# ======================================================================================================================
system_prompt: str = "Engkau adalah guru sejarah yang sangat sabar. Engkau terbiasa menjelaskan sesuatu dengan sangat panjang dan lengkap"
user_prompt: str = "Jelaskan siapakah ir. Soekarno itu? mengapa dia sangat terkenal di Indonesia?"

# ======================================================================================================================
# ChatGPTConnector Test
# ======================================================================================================================
print(f"{'\n' * 5}{'#' * 100}\n# Ask to ChatGPT\n{'#' * 100}")
chat_gpt = ChatGPTConnector(model=ChatGPTConnector.MODEL_gpt_4o)
result = chat_gpt.ask(system_prompt=system_prompt, user_prompt=user_prompt)
print(result)

# ======================================================================================================================
# ChatGPTConnector (Stream) Test
# ======================================================================================================================
print(f"{'\n' * 5}{'#' * 100}\n# Ask to ChatGPT (Stream result)\n{'#' * 100}")
chat_gpt = ChatGPTConnector(model=ChatGPTConnector.MODEL_gpt_4o)
result = chat_gpt.ask_with_stream_result(system_prompt=system_prompt, user_prompt=user_prompt)

for chunk in result:
    print(chunk.choices[0].delta.content or '', end="", flush=True)

# ======================================================================================================================
# ClaudeConnector Test
# ======================================================================================================================
print(f"{'\n' * 5}{'#' * 100}\n# Ask to Claude\n{'#' * 100}")
claude = ClaudeConnector()
result = claude.ask(system_prompt=system_prompt, user_prompt=user_prompt)
print(result)

# ======================================================================================================================
# ClaudeConnector (Stream Result) Test
# ======================================================================================================================
print(f"{'\n' * 5}{'#' * 100}\n# Ask to Claude (Stream result)\n{'#' * 100}")
claude = ClaudeConnector()
result = claude.ask_with_stream_result(system_prompt=system_prompt, user_prompt=user_prompt)
with result as stream:
    for text in stream.text_stream:
            print(text, end="", flush=True)


# ======================================================================================================================
# OllamaConnector Test
# ======================================================================================================================
print(f"{'\n' * 5}{'#' * 100}\n# Ask to Ollama\n{'#' * 100}")
ollama = OllamaConnector()
result = ollama.ask(system_prompt=system_prompt, user_prompt=user_prompt)
print(result)
