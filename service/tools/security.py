import base64
import hashlib
import calendar
import datetime
import jwt

from flask import current_app


def generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(generate_password_digest(password)).decode('utf-8')


def compare_passwords_hash(password_hash, other_password):
    return password_hash == generate_password_hash(other_password)


def generate_tokens(username, password, password_hash=None, is_refresh=False):
    if username is None:
        return None

    if not is_refresh:
        if not compare_passwords_hash(other_password=password, password_hash=password_hash):
            return None

    data = {
        "username": username,
        "password": password,
    }
    min_for_token = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data['exp'] = calendar.timegm(min_for_token.timetuple())
    access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])

    days_for_token = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=current_app.config['TOKEN_EXPIRE_DAYS'])
    data['exp'] = calendar.timegm(days_for_token.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])

    return {'access_token': access_token,
            'refresh_token': refresh_token}


def approve_refresh_token(refresh_token):
    data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['ALGORITHM'])
    username = data.get('username')
    password = data.get('password')

    return generate_tokens(username, password, is_refresh=True)
