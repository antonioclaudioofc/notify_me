from app.messaging.consumer import RabbitMQConsumer
from app.services.arena_manager_email_service import ArenaManagerEmailService


email_service = ArenaManagerEmailService()
consumer = RabbitMQConsumer(email_service)
consumer.start_consuming()
