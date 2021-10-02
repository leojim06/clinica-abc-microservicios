from flaskr import create_app
from flaskr.vistas.vistas import VistaSignIn, VistaLogIn, VistaAutorizador
from flaskr.modelos import db
from flask_jwt_extended import JWTManager
from flask_restful import Api

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaSignIn, '/signin'),
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaAutorizador, '/authorize')

jwt = JWTManager(app)
