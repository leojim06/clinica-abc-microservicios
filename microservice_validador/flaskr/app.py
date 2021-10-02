from flaskr import create_app
from flaskr.vistas.vistas import VistaValidadorHash
from flask_restful import Api

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaValidadorHash, '/validador-hash')
