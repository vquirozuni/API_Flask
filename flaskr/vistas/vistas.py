import socket
from flask_restful import Resource
from ..modelos import db, Bloqueado, BloqueadoSchema, User
from flask_jwt_extended import jwt_required, create_access_token
from flask import request
bloqueado_schema = BloqueadoSchema()


class Health(Resource):
    def get(self):
        return {"status": "OK"}, 200


class VistaBlackList(Resource):
    @jwt_required()
    def get(self):
        return [bloqueado_schema.dump(bloqueado) for bloqueado in Bloqueado.query.all()]

    @jwt_required()
    def post(self):
        _email = request.json["email"]
        _app_uuid = request.json["app_uuid"]
        _blocked_reason = request.json["blocked_reason"]

        if _email.strip() == "":
            return {"mensaje":"Ingrese el valor de email"}, 400

        if _app_uuid.strip() == "":
            return {"mensaje":"Ingrese el valor de app_uuid"}, 400

        bloqueado = Bloqueado.query.filter_by(email=_email).all()
        if bloqueado:
            return {"mensaje":"Email ya existe en la lista negra"}, 400
        
        _ip = request.remote_addr
        hostname = socket.gethostname()
        _ip = socket.gethostbyname(hostname)

        new_bloqueado = Bloqueado(email = _email, app_uuid = _app_uuid, blocked_reason = _blocked_reason, ip = _ip)
        db.session.add(new_bloqueado)
        db.session.commit()
        return {"mensaje":"Se registró email en la lista negra"}

class VistaBloqueado(Resource):
    @jwt_required()
    def get(self, email_bloqueado):
        bloqueado = Bloqueado.query.filter_by(email=email_bloqueado).first()
        if not bloqueado:
            return {"mensaje":"Email no existe en la lista negra"}, 400
        return bloqueado_schema.dump(bloqueado)

class VistaLogIn(Resource):
    def post(self):        
        u_username = request.json["username"]
        userName = User.query.filter_by(user_name=u_username).all()
        if not userName:
            return {"mensaje": "usuario o password incorrectos"}, 400

        u_password = request.json["password"]
        user = User.query.filter_by(user_name=u_username, password=u_password).all()
        if not user:
            return {"mensaje": "usuario o password incorrectos"}, 400

        token = create_access_token(identity=u_username)
        return {"token":token}