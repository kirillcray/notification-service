

def valid_email(email):
    if not email or not isinstance(email, str):
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    # Локальная часть и домен не должны быть пустыми
    if not parts[0] or not parts[1]:
        return False
    # В домене должна быть хотя бы одна точка
    if '.' not in parts[1]:
        return False
    # Домен не должен начинаться или заканчиваться точкой
    if parts[1].startswith('.') or parts[1].endswith('.'):
        return False

    return True


def valid_phone(phone: str) -> bool:

    if not phone or not isinstance(phone, str):
        return False

    # Должен начинаться с +
    if not phone.startswith('+'):
        return False

    # После + должны быть только цифры
    digits = phone[1:]  # убираем +

    return digits.isdigit() and len(digits) > 0


def valid_tg(username: str) -> bool:
    if not username or not isinstance(username, str):
        return False

    # Начинается с @ и больше 1
    return username.startswith('@') and len(username) > 1


def validate_notification(data):
    required_fields = ['type', 'recipient', 'message']
    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            return f"{field} is required"

    if data['type'] == 'email':
        if not valid_email(data['recipient']):
            return "Invalid email format"

    elif data['type'] == 'telegram':
        if not valid_tg(data['recipient']):
            return "Invalid tg username"

    elif data['type'] == 'sms':
        if not valid_phone(data['recipient']):
            return "Invalid phone number"
    else:
        return "Invalid type"
    return None
