import json
import logging
import os
from app import create_app
from app.broker import get_connection
from app.tasks import handle_notification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('worker')


def callback(ch, method, properties, body):
    # достаём id из сообщения и обрабатываем уведомление
    data = json.loads(body)
    notification_id = data['notification_id']
    logger.info(f"Получено: {notification_id}")
    handle_notification(notification_id)
    # Подтверждаем что сообщение обработано
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():

    queue_name = os.getenv('RABBITMQ_QUEUE', 'notifications')
    # flask нужен для работы с db через app_context
    app = create_app()
    with app.app_context():
        connection = get_connection()
        channel = connection.channel()
        # Настраиваем очередь
        channel.queue_declare(queue=queue_name, durable=True)
        # Начинам ее слушать, сообщения обрабатываем в callback
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        logger.info("Воркер запущен")
        # Бесконечно слушаем
        channel.start_consuming()


if __name__ == '__main__':
    main()
