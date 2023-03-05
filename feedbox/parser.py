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


def parse_atom(data, base_url=""):
    root = ET.fromstring(data)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entries = []
    for item in root.findall("a:entry", ns):
        link = next((node.get("href", "") for node in item.findall("a:link", ns)
                     if node.get("rel", "alternate") == "alternate"), "")
        title = item.findtext("a:title", "Untitled", ns).strip()
        entries.append({"key": item.findtext("a:id", "", ns).strip() or link or title,
                        "title": title, "url": urljoin(base_url, link),
                        "summary": item.findtext("a:summary", "", ns).strip()})
    return entries


def read_feed(data, base_url=""):
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError("Feed declarations are not supported")
    root = ET.fromstring(data)
    if root.tag == "{http://www.w3.org/2005/Atom}feed":
        return parse_atom(data, base_url)
    if root.tag != "rss":
        raise ValueError("Expected an RSS or Atom feed")
    return parse(data, base_url)
