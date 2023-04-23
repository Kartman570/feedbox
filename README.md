# feedbox

A small RSS and Atom inbox backed by SQLite. No account or browser needed.

## Run

Python 3.9 or newer; runtime uses only the standard library.

```sh
python3 -m feedbox import examples/news.xml --source workshop
python3 -m feedbox list --unread
python3 -m feedbox read 1
python3 -m feedbox export > inbox.json
python3 -m feedbox subscribe https://example.com/feed.xml
python3 -m feedbox refresh
```

Use `--db /path/to/inbox.sqlite3` before the command for another inbox.
Imports preserve read state and ignore repeated IDs within each source. Sources
have separate namespaces. Refresh keeps successful feeds when another fails and
returns a nonzero exit status if any failed. Export includes read state.

## Checks

```sh
python3 -m pip install -r requirements-dev.txt
make test
make lint
```

Tests use temporary SQLite databases and a loopback HTTP server. No public feeds
are required. Input XML must be UTF-8 and smaller than 2 MiB for HTTP imports.
This is a personal CLI, not a public URL-fetching service. Only subscribe to feeds
you trust. Article HTML is stored as text and never executed.
