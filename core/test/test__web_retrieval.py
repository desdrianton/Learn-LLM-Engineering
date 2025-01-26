from bs4 import BeautifulSoup

from core.web_retrieval import WebRetriever, Website


# ======================================================================================================================
# Test
# ======================================================================================================================
url_on_test = "https://www.prosigmaka.com"
web_retriever: WebRetriever = WebRetriever(url=url_on_test)
soup: BeautifulSoup = web_retriever.retrieve()
website: Website = Website(url=url_on_test, soup=soup)

print(website)
