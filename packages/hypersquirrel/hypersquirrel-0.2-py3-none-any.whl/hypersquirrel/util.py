from commmons import html
from lxml import html

import re

_non_numeric = re.compile(r'[^\d]+')


def html_from_url_with_headers(url, referer=None):
    return html.from_url(url, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Referer": referer or url
    })


def html_element_to_string(e):
    return html.tostring(e, encoding="utf-8").decode("utf-8")


def strip_non_numeric(s):
    return _non_numeric.sub('', s)
