from http.server import BaseHTTPRequestHandler, HTTPServer
from app.core.config import settings

from app.workers.arena_manager_worker import build_consumer as build_arena_consumer
from app.workers.antonio_claudio_dev_worker import build_consumer as build_portfolio_consumer


class HealthCheckHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            body = b"worker running"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()


def main():
    arena_consumer = build_arena_consumer()
    portfolio_consumer = build_portfolio_consumer()

    arena_consumer.start_in_thread()
    portfolio_consumer.start_in_thread()

    print("Both RabbitMQ consumers started")

    port = settings.PORT
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"Health check server listening on 0.0.0.0:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping consumers and health check server...")
    finally:
        server.server_close()
        arena_consumer.stop()
        portfolio_consumer.stop()


if __name__ == "__main__":
    main()
