from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# импортируем в конце, чтобы декораторы @api_bp.route зарегистрировались на api_bp
from app.api import notifications  # noqa: E402, F401
