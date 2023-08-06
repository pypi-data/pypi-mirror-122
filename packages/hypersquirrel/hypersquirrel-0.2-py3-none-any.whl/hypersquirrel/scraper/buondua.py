from commmons import html, head
from commmons.hash import md5
from commmons.url import get_host_url


def _get_file(a):
    href = a.attrib["href"]
    img = head(a.xpath("./img"))
    if img is not None:
        yield {
            "fileid": "bnd" + md5(href),
            "filename": img.attrib["alt"],
            "sourceurl": "vpr://" + get_host_url(a.base) + href,
            "thumbnailurl": img.attrib["data-src"]
        }


def scrape_buondua(url: str):
    root = html.from_url(url)
    for a in root.xpath("//a[contains(@class,'item-link')]"):
        yield from _get_file(a)
