import requests
from bs4 import BeautifulSoup


class DataSoup:

    def __init__(self, url: str, query: str):
        self.query = query
        self.url = url
        self.html_soup = self.make_soup()

    def make_soup(self):
        req = requests.get(str(self.url) + str(self.query))
        soup = BeautifulSoup(req.content, "html.parser")
        if req.status_code != 200:
            return None
        return soup
