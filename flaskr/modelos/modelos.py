from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

db = SQLAlchemy()

class Bloqueado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True)
    app_uuid = db.Column(db.String(20))
    ip = db.Column(db.String(20))
    blocked_reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class BloqueadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bloqueado
        include_relationships = True
        load_instance = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(50))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True