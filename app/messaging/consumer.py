import pika
import json
import threading
import traceback
import time
from typing import Callable

from app.core.config import settings


class RabbitMQConsumer:

    def __init__(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
        message_handler: Callable[[dict], None]
    ):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.message_handler = message_handler
        self.connection = None
        self.channel = None
        self.thread = None
        self.should_stop = False

    def _build_parameters(self) -> pika.URLParameters:
        params = pika.URLParameters(settings.RABBITMQ_URL)
        params.heartbeat = 30
        params.blocked_connection_timeout = 300
        params.connection_attempts = 3
        params.retry_delay = 5
        return params

    def connect(self):
        if not self.connection or self.connection.is_closed:
            print(
                f"[{self.queue_name}] Connecting to RabbitMQ...",
                flush=True,
            )

            self.connection = pika.BlockingConnection(self._build_parameters())
            self.channel = self.connection.channel()

            self.channel.basic_qos(prefetch_count=1)

            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='direct',
                durable=True
            )

            self.channel.queue_declare(
                queue=self.queue_name,
                durable=True
            )

            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.queue_name,
                routing_key=self.routing_key
            )

            print(
                f"[{self.queue_name}] Connected to RabbitMQ successfully",
                flush=True,
            )

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            print(f"[{self.queue_name}] Received message: {message}", flush=True)
            self.message_handler(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(
                f"[{self.queue_name}] Error processing message: {e}\n{traceback.format_exc()}",
                flush=True,
            )
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        while not self.should_stop:
            try:
                self.connect()

                self.channel.basic_consume(
                    queue=self.queue_name,
                    on_message_callback=self.callback,
                    auto_ack=False
                )

                print(
                    f"[{self.queue_name}] Waiting for messages...",
                    flush=True,
                )

                self.channel.start_consuming()
            except Exception as e:
                if self.should_stop:
                    break
                print(
                    f"[{self.queue_name}] Connection error: {e}\n{traceback.format_exc()}\nRetrying in 5 seconds...",
                    flush=True,
                )
                time.sleep(5)
            finally:
                try:
                    if self.channel and not self.channel.is_closed:
                        self.channel.close()
                except Exception:
                    pass
                try:
                    if self.connection and not self.connection.is_closed:
                        self.connection.close()
                except Exception:
                    pass

    def start_in_thread(self):
        self.thread = threading.Thread(
            target=self.start_consuming,
            daemon=True
        )

        self.thread.start()

        print(
            f"Consumer thread started for queue '{self.queue_name}'",
            flush=True,
        )

    def stop(self):
        self.should_stop = True
        try:
            if self.channel and self.channel.is_open:
                self.channel.stop_consuming()
        except Exception:
            pass
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
        except Exception:
            pass
        if self.thread:
            self.thread.join(timeout=10)
        print(f"Consumer stopped for queue '{self.queue_name}'", flush=True)
