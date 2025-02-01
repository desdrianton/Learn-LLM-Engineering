import json

from bs4 import BeautifulSoup

from core.agent import Agent
from core.llm_connector import LLMConnector
from core.web_retrieval import WebRetriever, Website


# ======================================================================================================================
# WebSummarizerAgent
# ======================================================================================================================
class BrochureMakerAgent(Agent):
    def __init__(self, llm_connector: LLMConnector):
        super().__init__(llm_connector=llm_connector)

    @staticmethod
    def _retrieve_page_content(url) -> Website:
        web_retriever: WebRetriever = WebRetriever(url=url)
        soup: BeautifulSoup = web_retriever.retrieve()
        return Website(url=url, soup=soup)

    def _step1_ask_llm_to_decide_what_are_the_most_important_links(self, whole_website_information: str):
        landing_page: Website = BrochureMakerAgent._retrieve_page_content(url=self._params["url"])
        whole_website_information += landing_page.__str__()

        system_prompt = "You are provided with a list of links found on a webpage. You are able to decide which of the links would be most relevant to include in a brochure about the company, such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
        system_prompt += "You should respond in JSON as in this example:"
        system_prompt += """{
            "links": [
                {"type": "about page", "url": "https://full.url/goes/here/about"},
                {"type": "careers page": "url": "https://another.full.url/careers"}
            ]
        }"""

        user_prompt = f"Here is the list of links on the website of {landing_page.get_url()} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(landing_page.get_links())

        return whole_website_information, json.loads(self._llm_connector.ask(system_prompt=system_prompt, user_prompt=user_prompt,
                                                                kwargs={"response_format_type": "json_object"}))

    def _step2_retrieve_important_pages(self, important_link, whole_website_information: str):
        for link in important_link:
            url = link["url"]
            page: Website = BrochureMakerAgent._retrieve_page_content(url=url)
            whole_website_information += "\n\n"
            whole_website_information += page.__str__()

        return whole_website_information

    def _step3_make_brochure(self, whole_website_information: str):
        company_name: str = self._params["company_name"] if "company_name" in self._params else None
        is_humorous: bool = (self._params["style"] and self._params["style"].lower() == "humorous") if "style" in self._params else False

        system_prompt_formal = "You are an assistant that analyzes the contents of several relevant pages from a company website and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown. Include details of company culture, customers and careers/jobs if you have the information."
        system_prompt_humorous = "You are an assistant that analyzes the contents of several relevant pages from a company website and creates a short humorous, entertaining, jokey brochure about the company for prospective customers, investors and recruits. Respond in markdown. Include details of company culture, customers and careers/jobs if you have the information."
        system_prompt = system_prompt_humorous if is_humorous else system_prompt_formal

        user_prompt = f"You are looking at a company called: {company_name}\n" if company_name else ""
        user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        user_prompt += whole_website_information
        user_prompt = user_prompt[:5_000]

        return self._llm_connector.ask(system_prompt=system_prompt, user_prompt=user_prompt)

    def act(self):
        whole_website_information = ""
        whole_website_information, important_links_json = self._step1_ask_llm_to_decide_what_are_the_most_important_links(whole_website_information)
        whole_website_information += self._step2_retrieve_important_pages(important_links_json["links"], whole_website_information)

        return self._step3_make_brochure(whole_website_information)
