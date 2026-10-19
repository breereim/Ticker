"""Dependency-free local driver panel for the JNJ valuation.

Run: .\\.venv\\Scripts\\python.exe .\\jnj_valuation_app.py
Then open http://127.0.0.1:8765.  Nothing is sent over the network.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Timer
from urllib.parse import urlparse
import webbrowser
import os

from jnj_project1_fcff import evaluate_model


ROOT = Path(__file__).resolve().parent
HTML = ROOT / "jnj_valuation_dashboard.html"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # Quiet, except for deliberate startup output.
        return

    def _send(self, status, body, content_type):
        encoded = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        route = urlparse(self.path).path
        if route in ("/", "/index.html"):
            self._send(200, HTML.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        elif route == "/api/model":
            self._send(200, json.dumps(evaluate_model()), "application/json")
        else:
            self._send(404, "Not found", "text/plain; charset=utf-8")

    def do_POST(self):
        if urlparse(self.path).path != "/api/model":
            self._send(404, "Not found", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(payload, dict):
                raise ValueError("Expected a JSON object of driver overrides.")
            self._send(200, json.dumps(evaluate_model(payload)), "application/json")
        except (ValueError, TypeError, AssertionError) as exc:
            self._send(400, json.dumps({"error": str(exc)}), "application/json")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = int(os.environ.get("JNJ_DASHBOARD_PORT", "8765"))
    print(f"JNJ valuation panel: http://{host}:{port}")
    print("Press Ctrl+C to stop. The app is local-only; no inputs leave this computer.")
    if os.environ.get("JNJ_OPEN_BROWSER", "1") != "0":
        Timer(0.5, lambda: webbrowser.open(f"http://{host}:{port}")).start()
    ThreadingHTTPServer((host, port), Handler).serve_forever()
