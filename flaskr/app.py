from flaskr import create_app
from flaskr.modelos.modelos import db
from flask_restful import Api
from flaskr.vistas.vistas import VistaBlackList, VistaBloqueado, VistaLogIn
from flaskr.vistas.vistas import Health
from flask_jwt_extended import JWTManager


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(Health, '/health')
api.add_resource(VistaBlackList, '/blacklists')
api.add_resource(VistaBloqueado, '/blacklists/<string:email_bloqueado>')
api.add_resource(VistaLogIn, '/auth/login')


jwt = JWTManager(app)