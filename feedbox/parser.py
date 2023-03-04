import xml.etree.ElementTree as ET
from urllib.parse import urljoin


def parse(data, base_url=""):
    root = ET.fromstring(data)
    entries = []
    for item in root.findall("./channel/item"):
        link = urljoin(base_url, item.findtext("link", "").strip())
        title = item.findtext("title", "Untitled").strip()
        identity = item.findtext("guid", "").strip() or link or title
        entries.append({"key": identity, "title": title, "url": link,
                        "summary": item.findtext("description", "").strip()})
    return entries
