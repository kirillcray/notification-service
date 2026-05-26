from flask import jsonify, request
from app.api import api_bp
from app.models import Notification
from app.extensions import db
from app.utils.validators import validate_notification
import logging

logger = logging.getLogger(__name__)


@api_bp.route("/notifications/<id>", methods=["GET"])
def get_notification(id):
    notification = db.session.get(Notification, id)
    if not notification:
        return jsonify({"error": "Not found"}), 404

    return (
        jsonify(
            {
                "id": notification.id,
                "status": notification.status,
                "error": notification.error_text,
            }
        ),
        200,
    )


@api_bp.route("/notifications", methods=["GET"])
def get_notifications():

    status = request.args.get("status")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    query = db.session.query(Notification)
    if status:
        query = query.filter(Notification.status == status)
    total = query.count()
    notifications = query.offset(offset).limit(limit)

    return (
        jsonify(
            {
                "total": total,
                "limit": limit,
                "offset": offset,
                "items": [n.to_dict() for n in notifications],
            }
        ),
        200,
    )


@api_bp.route("/notifications", methods=["POST"])
def post_notifications():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    error = validate_notification(data)

    if error:
        return jsonify({"error": error}), 400
    notification = Notification(
        type=data["type"],
        recipient=data["recipient"],
        subject=data.get("subject"),
        message=data["message"],
        status="pending",
        channel_data=data.get("channel_data"),
    )
    db.session.add(notification)
    db.session.commit()
    logger.info(
        f"Получен запрос на уведомление type={data['type']} recipient={data['recipient']}"
    )

    return jsonify({"id": notification.id, "status": "queued"}), 201
