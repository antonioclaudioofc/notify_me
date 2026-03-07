from app.core.config import settings
from app.messaging.consumer import RabbitMQConsumer
from app.services.antonio_claudio_dev.antonio_claudio_dev_email_service import AntonioClaudioDevEmailService


email_service = AntonioClaudioDevEmailService()


def handle_antonio_claudio_dev_message(message: dict):
    message_type = message.get("type")
    data = message.get("data")

    if message_type == "contact_message":
        email_service.send_message_from_payload(data)
    else:
        print(f"Unknown antonio claudio dev message type: {message_type}")


def build_consumer() -> RabbitMQConsumer:
    return RabbitMQConsumer(
        queue_name=settings.RABBITMQ_PORTFOLIO_QUEUE,
        exchange_name=settings.RABBITMQ_PORTFOLIO_EXCHANGE,
        routing_key=settings.RABBITMQ_PORTFOLIO_ROUTING_KEY,
        message_handler=handle_antonio_claudio_dev_message,
    )


def main():
    consumer = build_consumer()
    consumer.start_consuming()


if __name__ == "__main__":
    main()
