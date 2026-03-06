import pika
import json
import threading
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

    def connect(self):
        if not self.connection or self.connection.is_closed:
            connection_parameters = pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    username=settings.RABBITMQ_USERNAME,
                    password=settings.RABBITMQ_PASSWORD
                )
            )

            self.connection = pika.BlockingConnection(connection_parameters)

            self.channel = self.connection.channel()

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

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            print(f"Received message: {message}")
            self.message_handler(message)

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        self.connect()

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback,
            auto_ack=False
        )

        print('Starting RabbitMQ consumer...')

        self.channel.start_consuming()

    def start_in_thread(self):
        self.thread = threading.Thread(
            target=self.start_consuming,
            daemon=True
        )

        self.thread.start()

        print('Consumer started in background thread')

    def stop(self):
        if self.channel:
            self.channel.stop_consuming()
        if self.connection:
            self.connection.close()
        if self.thread:
            self.thread.join()
        print('Consumer stopped')
