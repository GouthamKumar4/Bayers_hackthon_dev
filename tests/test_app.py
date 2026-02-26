import json
import threading
import time
import unittest
from http.server import HTTPServer
from urllib.request import urlopen

from app.main import DemoHandler


class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = HTTPServer(("127.0.0.1", 8001), DemoHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def test_health_endpoint(self) -> None:
        with urlopen("http://127.0.0.1:8001/") as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["status"], "ok")

    def test_add_endpoint(self) -> None:
        with urlopen("http://127.0.0.1:8001/add/2/3") as response:
            payload = json.loads(response.read().decode("utf-8"))
        self.assertEqual(payload["result"], 5)


if __name__ == "__main__":
    unittest.main()
