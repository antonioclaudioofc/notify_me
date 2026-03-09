from http.server import BaseHTTPRequestHandler, HTTPServer
from app.core.config import settings

from app.workers.arena_manager_worker import build_consumer as build_arena_consumer
from app.workers.antonio_claudio_dev_worker import build_consumer as build_portfolio_consumer


class HealthCheckHandler(BaseHTTPRequestHandler):

    def _send_ok(self, include_body: bool = True):
        body = b"worker running"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._send_ok(include_body=True)
            return

        self.send_response(404)
        self.end_headers()

    def do_HEAD(self):
        if self.path == "/":
            self._send_ok(include_body=False)
            return

        self.send_response(404)
        self.end_headers()


def main():
    arena_consumer = build_arena_consumer()
    portfolio_consumer = build_portfolio_consumer()

    print("Starting RabbitMQ consumers...", flush=True)
    arena_consumer.start_in_thread()
    portfolio_consumer.start_in_thread()

    print("Both RabbitMQ consumers started", flush=True)

    port = settings.PORT
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"Health check server listening on 0.0.0.0:{port}", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping consumers and health check server...", flush=True)
    finally:
        server.server_close()
        arena_consumer.stop()
        portfolio_consumer.stop()


if __name__ == "__main__":
    main()
