from llm_connector import ChatGPTConnector, OllamaConnector

# ======================================================================================================================
# Prepare
# ======================================================================================================================
system_prompt: str = ""
user_prompt: str = "Sekarang hari apa? tanggal berapa?"

# ======================================================================================================================
# ChatGPTConnector Test
# ======================================================================================================================
print(f"================================================== Ask to ChatGPT")
chat_gpt = ChatGPTConnector()
result = chat_gpt.ask(system_prompt=system_prompt, user_prompt=user_prompt)
print(result)

# ======================================================================================================================
# OllamaConnector Test
# ======================================================================================================================
print(f"================================================== Ask to Ollama")
ollama = OllamaConnector()
result = ollama.ask(system_prompt=system_prompt, user_prompt=user_prompt)
print(result)
