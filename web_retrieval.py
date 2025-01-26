from typing import *

from bs4 import BeautifulSoup
from requests import *

# ======================================================================================================================
# WebRetriever
# ======================================================================================================================
class WebRetriever:
    _HEADERS: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    _url : str = None
    _res: Response = None
    _soup: BeautifulSoup = None


    def __init__(self, *, url : str):
        self._url = url


    def retrieve(self):
        self._res = get(self._url, headers=self._HEADERS)
        self._soup = BeautifulSoup(self._res.content, "html.parser")

        return self._soup


    def get_url(self) -> str:
        return self._url


    def get_soup(self) -> BeautifulSoup:
        return self._soup


# ======================================================================================================================
# Website
# ======================================================================================================================
class Website:
    _url: str = None
    _soup: BeautifulSoup = None
    _title: str = None
    _body: str = None
    _links: Set[str] = None


    def __init__(self, *, url : str, soup : BeautifulSoup):
        self._url = url
        self._soup = soup
        self._parsing()
        self._generate_links()


    def __str__(self) -> str:
        result = f""
        result += f"Url: {self._url}\n"
        result += f"Title: {self._title}\n"
        result += f"Body: {self._body}\n"

        return result


    def _parsing(self):
        self._title = self._soup.title.string if self._soup.title else "No title found"
        for irrelevant in self._soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self._body = self._soup.body.get_text(separator="\n", strip=True)


    def _generate_links(self) -> Set[str]:
        self._links = {link.get("href") for link in self._soup.find_all("a")}

        return self._links


    def get_url(self) -> str:
        return self._url


    def get_soup(self) -> BeautifulSoup:
        return self._soup


    def get_title(self) -> str:
        return self._title


    def get_body(self) -> str:
        return self._body


    def get_links(self) -> Set[str]:
        return self._links
