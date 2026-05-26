import uuid
from datetime import datetime, timezone
from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )  # UUID
    type = db.Column(db.String(20), nullable=False)  # тг, смс, емейл и тп.
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255))  # Тема
    message = db.Column(db.Text, nullable=False)
    channel_data = db.Column(db.JSON)
    status = db.Column(db.String(20), nullable=False, default="pending")
    error_text = db.Column(db.Text)  # текст ошибки при неудачной отпавке

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "recipient": self.recipient,
            "subject": self.subject,
            "message": self.message,
            "status": self.status,
            "error_text": self.error_text,
            "channel_data": self.channel_data,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
