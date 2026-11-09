import http.server
import json
import time
import os

STATUS_PATH = os.path.join(os.path.dirname(__file__), "status.json")
PORT = 8765

SPINNER_FRAMES = ["·", "✻", "✽", "✶", "✳", "✢"]


def fmt_elapsed(start):
    secs = max(0, int(time.time() - start))
    m, s = divmod(secs, 60)
    return f"{m}:{s:02d}"


def read_status():
    try:
        with open(STATUS_PATH, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return {"state": "idle", "verb": "", "start": time.time()}


def render():
    status = read_status()
    state = status.get("state", "idle")
    start = status.get("start", time.time())

    if state == "thinking":
        frame = SPINNER_FRAMES[int(time.time()) % len(SPINNER_FRAMES)]
        verb = status.get("verb", "Working")
        return f"{frame} {verb}… ({fmt_elapsed(start)})"
    elif state == "waiting":
        frame = SPINNER_FRAMES[int(time.time() * 2) % len(SPINNER_FRAMES)]
        return f"{frame} needs you ({fmt_elapsed(start)})"
    else:
        return "\U0001F4A4 idle"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            body = render().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
