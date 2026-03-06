from app.messaging.consumer import RabbitMQConsumer
from app.core.config import settings
from app.services.arena_manager.arena_manager_email_service import ArenaManagerEmailService


email_service = ArenaManagerEmailService()


def handle_arena_manager_message(message: dict):
    message_type = message.get("type")
    data = message.get("data")

    if message_type == "verification":
        email_service.send_verification_email(data)
    elif message_type == "owner_promotion":
        email_service.send_owner_promotion_email(data["user"], data["arena"])
    elif message_type == "new_court":
        email_service.send_new_court_email(
            data["user"], data["arena"], data["court"])
    elif message_type == "reservation_created":
        email_service.send_reservation_created_email(data)
    elif message_type == "reservation_cancelled":
        email_service.send_reservation_cancelled_email(data)
    else:
        print(f"Unknown arena manager message type: {message_type}")


consumer = RabbitMQConsumer(
    queue_name=settings.RABBITMQ_ARENA_MANAGER_QUEUE,
    exchange_name=settings.RABBITMQ_ARENA_MANAGER_EXCHANGE,
    routing_key=settings.RABBITMQ_ARENA_MANAGER_ROUTING_KEY,
    message_handler=handle_arena_manager_message
)

consumer.start_consuming()
