import jwt
from flask import request, current_app

from implemented import user_service


def auth_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.environ.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')

        if not token:
            return "Token out of header"

        try:
            jwt.decode(token, key=current_app.config['SECRET_KEY'], algorithms=current_app.config['ALGORITHM'])

            return func(*args, **kwargs)

        except Exception as e:
            print(e)
            return "Invalid token"

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.environ.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')

        if not token:
            return "Token out of header"

        try:
            data = jwt.decode(token, key=current_app.config['SECRET_KEY'], algorithms=current_app.config['ALGORITHM'])
            user = user_service.get_user_by_login(data.get("username"))

            if user:
                if not user.role == 'admin':
                    return "Access denied"

            return func(*args, **kwargs)

        except Exception as e:
            print(e)
            return "Invalid token"

    return wrapper
