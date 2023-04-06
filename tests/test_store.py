import tempfile
import unittest
from pathlib import Path
from feedbox.store import Inbox


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "inbox.db"
        self.inbox = Inbox(self.path)
        self.entry = {"key": "a", "title": "A", "url": "/a", "summary": ""}

    def tearDown(self):
        self.inbox.close()
        self.tmp.cleanup()

    def test_duplicates_and_sources(self):
        self.assertEqual(self.inbox.ingest("one", [self.entry, self.entry]), 1)
        self.assertEqual(self.inbox.ingest("two", [self.entry]), 1)
        self.assertEqual(len(self.inbox.entries(source="one")), 1)

    def test_read_persists(self):
        self.inbox.ingest("one", [self.entry])
        self.assertTrue(self.inbox.mark(1))
        self.inbox.close()
        self.inbox = Inbox(self.path)
        self.assertEqual(self.inbox.entries(unread=True), [])
        self.assertFalse(self.inbox.mark(99))

    def test_subscriptions(self):
        self.inbox.subscribe("https://example.com/feed")
        self.inbox.subscribe("https://example.com/feed")
        self.assertEqual(len(self.inbox.feeds()), 1)
        self.inbox.unsubscribe("https://example.com/feed")
        self.assertEqual(self.inbox.feeds(), [])
