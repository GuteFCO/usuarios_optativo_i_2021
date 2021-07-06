import jwt
from functools import wraps
from werkzeug.exceptions import Unauthorized
from flask import current_app, request
from .models import Usuario


def autorizar(f):
    @wraps(f)
    def autorizada(*args, **kwargs):
        usuario = get_usuario_request()
        if not usuario:
            raise Unauthorized
        return f(usuario, *args, **kwargs)
    return autorizada


def log(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_app.config['LOG']:
            print('***************')
            print(f.__name__)
            print(*args)
            print(**kwargs)
        value = f(*args, **kwargs)
        if current_app.config['LOG']:
            print(value)
        return value
    return wrapper


def check_usuario():
    usuario_request = get_usuario_request()
    if not usuario_request:
        raise Unauthorized

    return usuario_request


def get_usuario_request():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return False

    partes = auth_header.split(' ')

    if len(partes) != 2:
        return False

    token = partes[1]

    secret = '123ABC'

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])

        usuario_id = payload['sub']

        usuario = Usuario.query.get(usuario_id)

        if usuario is None:
            return False

        return usuario
    except Exception as e:
        print(e)
        return False
