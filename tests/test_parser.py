import unittest
from feedbox.parser import read_feed


class ParserTests(unittest.TestCase):
    def test_rss(self):
        data = b'<rss><channel><item><title>One</title><link>/one</link></item></channel></rss>'
        self.assertEqual(read_feed(data, "https://example.com")[0]['url'],
                         "https://example.com/one")

    def test_atom(self):
        data = (b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>a</id>'
                b'<title>A</title><link href="/a"/></entry></feed>')
        self.assertEqual(read_feed(data, "https://example.com")[0]['key'], "a")

    def test_unknown_format(self):
        with self.assertRaises(ValueError):
            read_feed(b'<html/>')

    def test_declarations(self):
        with self.assertRaises(ValueError):
            read_feed(b'<!DOCTYPE rss><rss/>')

    def test_empty_rss(self):
        self.assertEqual(read_feed(b'<rss><channel/></rss>'), [])
