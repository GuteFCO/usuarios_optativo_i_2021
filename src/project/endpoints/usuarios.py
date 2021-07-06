import jwt
from functools import wraps
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import Forbidden, NotFound
from project.models import Usuario
from project.decorators import autorizar, log
from project.serializers import UsuarioSchema
from project import db, bcrypt


blueprint = Blueprint('usuarios', __name__)


@blueprint.route('/usuarios', methods=['POST'])
def index():
    usuario = UsuarioSchema().load(request.json)

    # Usuario(nombre='Francisco', password='1234', .....)
    #usuario = Usuario(**datos)

    #usuario = Usuario(datos['nombre'], datos['email'], datos['password'])
    #usuario = Usuario(
    #    email=datos['email'], nombre=datos['nombre'], password=datos['password'])

    db.session.add(usuario)
    db.session.commit()

    return UsuarioSchema().dump(usuario), 201


@blueprint.route('/usuarios', methods=['GET'])
@autorizar
@log
def listar_usuarios(usuario):
    usuarios = Usuario.query.all()

    return jsonify(UsuarioSchema().dump(usuarios, many=True)), 200


@blueprint.route('/usuarios/<id>', methods=['GET'])
@autorizar
def obtener_usuario(usuario, id):
    if str(usuario.id) != id:
        raise Forbidden

    usuario_encontrado = Usuario.query.get_or_404(id)
    #usuario_encontrado = Usuario.query.filter_by(id=id).first()

    #if not usuario_encontrado:
    #    raise NotFound

    #if not usuario_encontrado:
    #    return 'Not found', 404

    return UsuarioSchema().dump(usuario_encontrado), 200


@blueprint.route('/usuarios/<id>', methods=['PUT'])
@autorizar
def actualizar_usuario(usuario, id):
    if str(usuario.id) != id:
        raise Forbidden

    usuario_encontrado = Usuario.query.get_or_404(id)

    usuario_encontrado = UsuarioSchema().load(
        request.json,
        instance=usuario_encontrado)

    #usuario_encontrado.nombre = datos['nombre']
    #usuario_encontrado.email = datos['email']
    #usuario_encontrado.password = datos['password']
    #usuario_encontrado.direccion = datos['direccion']

    db.session.add(usuario_encontrado)
    db.session.commit()

    return UsuarioSchema().dump(usuario_encontrado), 200


@blueprint.route('/usuarios/<id>', methods=['PATCH'])
@autorizar
def parchar_usuario(usuario, id):
    if str(usuario.id) != id:
        raise Forbidden

    usuario_encontrado = Usuario.query.get_or_404(id)

    usuario_encontrado = UsuarioSchema().load(
        request.json,
        instance=usuario_encontrado,
        partial=True)

    db.session.add(usuario_encontrado)
    db.session.commit()

    return UsuarioSchema().dump(usuario_encontrado), 200


@blueprint.route('/usuarios/<id>', methods=['DELETE'])
@autorizar
def eliminar_usuario(usuario, id):
    if str(usuario.id) != id:
        raise Forbidden

    usuario_encontrado = Usuario.query.get_or_404(id)

    db.session.delete(usuario_encontrado)
    db.session.commit()

    return '', 204


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    datos = request.get_json()

    usuario = Usuario.query.filter_by(
        email=datos['email']).first()

    if usuario is None:
        raise NotFound

    if not bcrypt.check_password_hash(usuario.password, datos['password']):
        raise NotFound

    secret = '123ABC'

    payload = {
        'sub': usuario.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() +  timedelta(days=1)
    }

    return jwt.encode(payload, secret, algorithm='HS256')


@blueprint.route('/usuario_actual', methods=['GET'])
@autorizar
def obtener_usuario_actual(usuario):
    return UsuarioSchema().dump(usuario), 200
