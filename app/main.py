import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


class DemoHandler(BaseHTTPRequestHandler):
    def _write_json(self, payload: dict, status_code: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/":
            self._write_json({"status": "ok", "service": "bayers-devsecops-demo"})
            return

        parts = path.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "add":
            try:
                a, b = int(parts[1]), int(parts[2])
                self._write_json({"a": a, "b": b, "result": a + b})
                return
            except ValueError:
                pass

        self._write_json({"error": "not found"}, status_code=404)


def run() -> None:
    server = HTTPServer(("0.0.0.0", 8000), DemoHandler)
    print("Server running on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
