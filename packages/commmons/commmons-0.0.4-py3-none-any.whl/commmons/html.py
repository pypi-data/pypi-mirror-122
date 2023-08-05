import requests
from lxml import html
from lxml.html import HtmlElement


def from_url(url, **kwargs) -> HtmlElement:
    r = requests.get(url, **kwargs)
    r.raise_for_status()
    return html.fromstring(r.text)
