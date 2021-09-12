from microservice_registrar_paciente import create_app
from .modelos import db
from flask_restful import Api
from .vistas import VistaRegistrarPaciente
import requests
from flask import jsonify


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaRegistrarPaciente, '/paciente')

@app.route('/echo/<nodo>', methods=['GET'])
def echo(nodo=None):
    data = {'estado: ' + nodo: 'ok'}
    return jsonify(data), 200