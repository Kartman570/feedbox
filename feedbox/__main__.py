import argparse
import json
import sys
from pathlib import Path
from urllib.error import URLError
from xml.etree.ElementTree import ParseError

from .fetch import MAX_BYTES, fetch
from .parser import read_feed
from .store import Inbox


def main():
    parser = argparse.ArgumentParser(description="A local feed inbox")
    parser.add_argument("--db", default="feedbox.sqlite3")
    commands = parser.add_subparsers(dest="command", required=True)
    imp = commands.add_parser("import")
    imp.add_argument("file", type=Path)
    imp.add_argument("--source", default="local")
    listing = commands.add_parser("list")
    listing.add_argument("--unread", action="store_true")
    listing.add_argument("--source")
    listing.add_argument("--limit", type=int, default=50)
    mark = commands.add_parser("read")
    mark.add_argument("id", type=int)
    for name in ("subscribe", "unsubscribe"):
        commands.add_parser(name).add_argument("url")
    commands.add_parser("feeds")
    commands.add_parser("refresh")
    commands.add_parser("export")
    args = parser.parse_args()
    inbox = Inbox(args.db)
    try:
        if args.command == "import":
            with args.file.open("rb") as stream:
                data = stream.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("Feed is larger than 2 MiB")
            print(inbox.ingest(args.source, read_feed(data)))
        elif args.command == "list":
            if args.limit < 1:
                raise ValueError("Limit must be positive")
            for entry in inbox.entries(args.unread, args.source, args.limit):
                print("{id}: {title}\n  {url}".format(**entry))
        elif args.command == "read":
            if not inbox.mark(args.id):
                raise ValueError("Entry not found")
        elif args.command == "subscribe":
            from urllib.parse import urlsplit
            if urlsplit(args.url).scheme not in ("http", "https"):
                raise ValueError("Feed URL must use http or https")
            inbox.subscribe(args.url)
        elif args.command == "unsubscribe":
            inbox.unsubscribe(args.url)
        elif args.command == "feeds":
            print("\n".join(inbox.feeds()))
        elif args.command == "refresh":
            failed = False
            for url in inbox.feeds():
                try:
                    print(url, inbox.ingest(url, fetch(url)))
                except (OSError, URLError, ValueError, ParseError) as error:
                    print(str(error), file=sys.stderr)
                    failed = True
            return int(failed)
        elif args.command == "export":
            print(json.dumps(inbox.entries(limit=-1), indent=2))
    except (OSError, ValueError, ParseError) as error:
        print(str(error), file=sys.stderr)
        return 1
    finally:
        inbox.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
