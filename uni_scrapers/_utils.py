from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl
from functools import wraps
import re

ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}

def scrape_page(base_url):
    return BeautifulSoup(
        urlopen(Request(base_url, headers=HEADERS)).read(),
        "lxml"
    )

def on_exception_return(to_return):
    """
    On unpredicted exception return `to_return` provided in the decorator.
    Still raise some specific errors (as NotImplementedError listed here)
    This is needed due to not being able to predict what elements can be missing
    from the DOM and not being able to foresee all the possible erorrs from bs4
    """
    def decorate(decorated_function):
        @wraps(decorated_function)
        def wrap(*args, **kwargs):
            try:
                result = decorated_function(*args, **kwargs)
                return result
            except NotImplementedError as e:
                raise e
            except Exception:
                return to_return
        return wrap
    return decorate