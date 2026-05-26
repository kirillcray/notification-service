import json
import os
import logging
import pika

logger = logging.getLogger(__name__)


def get_connection():
    """Открывает соединение с RabbitMQ по URL из переменных окружения."""
    url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
    params = pika.URLParameters(url)
    return pika.BlockingConnection(params)


def publish_notification(notification_id):
    """Кладёт id уведомления в очередь для последующей обработки воркером."""
    queue_name = os.getenv('RABBITMQ_QUEUE', 'notifications')
    connection = get_connection()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        message = json.dumps({'notification_id': notification_id})
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json',
            )
        )
        logger.info(
            f"Опубликовано в очередь: notification_id={notification_id}")
    finally:
        connection.close()
