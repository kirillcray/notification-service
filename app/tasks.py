import logging

from app.extensions import db
from app.models import Notification

logger = logging.getLogger(__name__)


def send_email(notification):
    logger.info(f"[EMAIL]: {notification.recipient}: {notification.subject}")


def send_telegram(notification):
    logger.info(
        f"[TELEGRAM]: {notification.recipient}: {notification.message}")


def send_sms(notification):
    logger.info(f"[SMS]: {notification.recipient}")


def handle_notification(notification_id):
    notification = db.session.get(Notification, notification_id)
    if not notification:
        logger.warning(f"Уведомление не найдено: {notification_id}")
        return
    try:
        if notification.type == 'email':
            send_email(notification)
        elif notification.type == 'telegram':
            send_telegram(notification)
        elif notification.type == 'sms':
            send_sms(notification)
        notification.status = 'sent'
        db.session.commit()
        logger.info(f"Уведомление отправлено: id={notification_id}")
    except Exception as e:
        notification.status = 'failed'
        notification.error_text = str(e)
        db.session.commit()
        logger.error(f"Ошибка отправки {notification_id}: {e}")
