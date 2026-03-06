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


consumer = RabbitMQConsumer(
    queue_name=settings.RABBITMQ_PORTFOLIO_QUEUE,
    exchange_name=settings.RABBITMQ_PORTFOLIO_EXCHANGE,
    routing_key=settings.RABBITMQ_PORTFOLIO_ROUTING_KEY,
    message_handler=handle_antonio_claudio_dev_message
)

consumer.start_consuming()
