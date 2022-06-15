import hashlib

from datetime import datetime, timedelta
import jwt
import calendar

from flask import request, abort

SECRET_HERE = '249y823r9v8238r9u'
JWT_ALGORITHM = 'HS256'


def get_hash(password):
    """
    конвертирует полученный пароль в хэш пароля
    """
    password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_hash


def generate_tokens(data):
    """
    генерирует access_token, refresh_token в виде словаря
    """
    min30 = datetime.utcnow() + timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    data["refresh_token"] = False
    access_token = jwt.encode(payload=data, key=SECRET_HERE, algorithm=JWT_ALGORITHM)

    days30 = datetime.utcnow() + timedelta(days=30)
    data["exp"] = calendar.timegm(days30.timetuple())
    data["refresh_token"] = True
    refresh_token = jwt.encode(payload=data, key=SECRET_HERE, algorithm=JWT_ALGORITHM)

    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens


def decode_token(token):
    """
    общая функция декодирования токена по секретному ключу и алгоритму
    """
    try:
        decoded_token = jwt.decode(jwt=token, key=SECRET_HERE, algorithms=[JWT_ALGORITHM])
        return decoded_token

    except Exception as e:
        abort(400)


def auth_required(func):
    """
    запрашивает авторизацию пользователя
    """
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        decoded_token_ = decode_token(token)

        if decoded_token_["refresh_token"]:
            abort(400)

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """
    проверяет роль пользователя на соотв. администратору
    """
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        decoded_token_ = decode_token(token)

        if decoded_token_["role"] != "admin":
            abort(403)

        return func(*args, **kwargs)
    return wrapper
