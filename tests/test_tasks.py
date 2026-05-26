from unittest.mock import patch
from app.extensions import db
from app.models import Notification
from app.tasks import handle_notification


def test_handle_notification_sent(app):

    # кладём уведомление в БД
    n = Notification(
        id='test-id-1',
        type='email',
        recipient='test@example.com',
        message='Привет',
        status='pending',
    )
    db.session.add(n)
    db.session.commit()
    handle_notification('test-id-1')
    updated = db.session.get(Notification, 'test-id-1')
    assert updated.status == 'sent'
    assert updated.error_text is None


def test_handle_notification_failed(app):

    n = Notification(
        id='test-id-2',
        type='email',
        recipient='test@example.com',
        message='Привет',
        status='pending',
    )
    db.session.add(n)
    db.session.commit()
    # притворяемся, что send_email падает
    with patch('app.tasks.send_email', side_effect=Exception('boom')):
        handle_notification('test-id-2')
    updated = db.session.get(Notification, 'test-id-2')
    assert updated.status == 'failed'
    assert 'boom' in updated.error_text
