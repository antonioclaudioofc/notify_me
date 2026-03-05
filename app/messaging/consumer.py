import pika
import json
import threading

from app.core.config import settings
from app.services.email_service import EmailService


class RabbitMQConsumer:

    def __init__(self, email_service: EmailService):
        self.email_service = email_service
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
                exchange=settings.RABBITMQ_EXCHANGE,
                exchange_type='direct',
                durable=True
            )

            self.channel.queue_declare(
                queue=settings.RABBITMQ_QUEUE,
                durable=True
            )

            self.channel.queue_bind(
                exchange=settings.RABBITMQ_EXCHANGE,
                queue=settings.RABBITMQ_QUEUE,
                routing_key='arena_manager'
            )

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            print(f"Received message: {message}")
            message_type = message.get("type")
            data = message.get("data")

            if message_type == "verification":
                self.email_service.send_verification_email(data)
            elif message_type == "owner_promotion":
                self.email_service.send_owner_promotion_email(
                    data["user"], data["arena"])
            elif message_type == "new_court":
                self.email_service.send_new_court_email(
                    data["user"], data["arena"], data["court"])
            elif message_type == "reservation_created":
                self.email_service.send_reservation_created_email(data)
            elif message_type == "reservation_cancelled":
                self.email_service.send_reservation_cancelled_email(data)
            else:
                print(f"Unknown message type: {message_type}")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        self.connect()
        self.channel.basic_consume(
            queue=settings.RABBITMQ_QUEUE,
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


def run_worker(email_service: EmailService):
    consumer = RabbitMQConsumer(email_service)
    consumer.start_consuming()
