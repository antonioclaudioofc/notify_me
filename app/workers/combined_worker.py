import time

from app.workers.arena_manager_worker import build_consumer as build_arena_consumer
from app.workers.antonio_claudio_dev_worker import build_consumer as build_portfolio_consumer


def main():
    arena_consumer = build_arena_consumer()
    portfolio_consumer = build_portfolio_consumer()

    arena_consumer.start_in_thread()
    portfolio_consumer.start_in_thread()

    print("Both RabbitMQ consumers started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping consumers...")
        arena_consumer.stop()
        portfolio_consumer.stop()


if __name__ == "__main__":
    main()
