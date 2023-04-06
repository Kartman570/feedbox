import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from feedbox.fetch import fetch


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<rss><channel><item><title>Local</title></item></channel></rss>')

    def log_message(self, *args):
        pass


class FetchTests(unittest.TestCase):
    def test_http_feed(self):
        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            items = fetch("http://127.0.0.1:%s/feed" % server.server_port)
            self.assertEqual(items[0]['title'], "Local")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_reject_local_scheme(self):
        with self.assertRaises(ValueError):
            fetch("file:///etc/passwd")
