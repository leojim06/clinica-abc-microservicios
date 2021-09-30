from microservice_registrar_paciente.vistas.vistas import VistaPaciente, VistaHistoriaClinicaPaciente, VistaRegistroHistoriaClinica
from microservice_registrar_paciente.modelos import db
from microservice_registrar_paciente import create_app
from flask_restful import Api
from flask import jsonify


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
# Servicio registrar nuevo paciente
api.add_resource(VistaPaciente, '/paciente')
# Servicio ConsultarInformacionPaciente
api.add_resource(VistaHistoriaClinicaPaciente, '/paciente/<int:id_paciente>/historia-clinica')
# Servicio RegistrarHistoriaClinicaPaciente
api.add_resource(VistaRegistroHistoriaClinica, '/historia-clinica/<int:id_historia_clinica>/registro')

@app.route('/echo/<nodo>', methods=['GET'])
def echo(nodo=None):
    data = {'estado: ' + nodo: 'ok'}
    return jsonify(data), 200