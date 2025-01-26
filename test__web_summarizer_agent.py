from llm_connector import LLMConnector, ChatGPTConnector, OllamaConnector
from web_summarizer_agent import WebSummarizerAgent

# ======================================================================================================================
# Test
# ======================================================================================================================
url_on_test = "https://www.prodemy.id"
# llm_connector: LLMConnector = ChatGPTConnector()
llm_connector: LLMConnector = OllamaConnector()
web_summarizer_agent: WebSummarizerAgent = WebSummarizerAgent(llm_connector=llm_connector)
answer: str = web_summarizer_agent.with_params({"url": url_on_test}).act()
print(answer)
