from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}


def scrape_page(page_source, driver_source=False):

    if driver_source:
        return BeautifulSoup(
            page_source,
            "html.parser"
        )
    else:
        page = None
        if os.getenv('TESTING', 'false').lower() == 'false':
            print('If page is large, this might take a while :(')

        with urlopen(Request(page_source, headers=HEADERS)) as response:
            page = response.read()

        return BeautifulSoup(
            page,
            "html.parser"
        )
