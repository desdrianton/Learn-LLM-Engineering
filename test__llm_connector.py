from llm_connector import ChatGPTConnector, OllamaConnector
from web_retrieval import WebRetriever, Website

# ======================================================================================================================
# Prepare
# ======================================================================================================================
# url_on_test: str = "https://www.prosigmaka.com"
url_on_test: str = "https://www.detik.com"

print(f"================================================== Retrieving: {url_on_test}")
web_retriever = WebRetriever(url=url_on_test)
soup = web_retriever.retrieve()

print(f"================================================== Parsing")
website = Website(url=url_on_test, soup=soup)

system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown. Please use indonesian language to summarize"

user_prompt = f"You are looking at a website titled {website.get_title()}"
user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n"
user_prompt += "\nPlease use indonesian language to summarize"
user_prompt += website.get_body()

print(f"================================================== prompt")
print(f"System prompt: {system_prompt}\n")
print(f"User prompt: {user_prompt}\n")

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
