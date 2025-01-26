from brochure_maker_agent import BrochureMakerAgent
from llm_connector import ChatGPTConnector

# ======================================================================================================================
# Test
# ======================================================================================================================
# url_on_test = "https://www.detik.com"
url_on_test = "https://www.prosigmaka.com"

llm_connector = ChatGPTConnector()
agent = BrochureMakerAgent(llm_connector)

llm_answer = agent.with_params(
    {"url": url_on_test, "company_name": "PT. Pro Sigmaka Mandiri", "style": "humorous"}).act()
print(llm_answer)
