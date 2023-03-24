from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .parser import read_feed


MAX_BYTES = 2 * 1024 * 1024


def fetch(url, timeout=10):
    if urlsplit(url).scheme not in ("http", "https"):
        raise ValueError("Feed URL must use http or https")
    request = Request(url, headers={"User-Agent": "feedbox"})
    with urlopen(request, timeout=timeout) as response:
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Feed is larger than 2 MiB")
        return read_feed(data, response.url)
