import sqlite3


class Inbox:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY, source TEXT NOT NULL, entry_key TEXT NOT NULL,
                title TEXT NOT NULL, url TEXT NOT NULL, summary TEXT NOT NULL,
                seen INTEGER NOT NULL DEFAULT 0, UNIQUE(source, entry_key)
            );
        """)

    def ingest(self, source, entries):
        added = 0
        with self.db:
            for entry in entries:
                cursor = self.db.execute(
                    "INSERT OR IGNORE INTO entries(source,entry_key,title,url,summary) "
                    "VALUES(?,?,?,?,?)",
                    (source, entry['key'], entry['title'], entry['url'], entry['summary']))
                added += cursor.rowcount
        return added

    def close(self):
        self.db.close()
