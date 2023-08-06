import uuid

from commmons import html


def scrape_gimg(url):
    root = html.from_url(url)
    for img in root.xpath("//img[@src]"):
        yield {
            "fileid": str(uuid.uuid4()),
            "filename": str(uuid.uuid4()),
            "sourceurl": str(uuid.uuid4()),
            "thumbnailurl": img.attrib["src"]
        }
