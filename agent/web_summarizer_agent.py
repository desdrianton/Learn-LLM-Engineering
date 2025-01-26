from bs4 import BeautifulSoup

from core.agent import Agent
from core.llm_connector import LLMConnector
from core.web_retrieval import WebRetriever, Website


# ======================================================================================================================
# WebSummarizerAgent
# ======================================================================================================================
class WebSummarizerAgent(Agent):
    def __init__(self, llm_connector: LLMConnector):
        super().__init__(llm_connector)

    def _generate_system_prompt(self) -> str:
        return "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown. Please use indonesian language to summarize"

    def _generate_user_prompt(self) -> str:
        user_prompt = f"You are looking at a website titled {self._params["title"]}"
        user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n"
        user_prompt += "\nPlease use indonesian language to summarize"
        user_prompt += self._params["body"]

        return user_prompt

    def _retrieve_website(self):
        url: str = self._params.get("url")
        web_retriever: WebRetriever = WebRetriever(url=url)
        soup: BeautifulSoup = web_retriever.retrieve()
        website: Website = Website(url=url, soup=soup)
        self._params["title"] = website.get_title()
        self._params["body"] = website.get_body()

    def act(self):
        self._retrieve_website()

        return self._llm_connector.ask(system_prompt=self._generate_system_prompt(),
                                       user_prompt=self._generate_user_prompt())
