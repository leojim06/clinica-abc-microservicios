from ..modelos import db, Paciente, PacienteSchema
from flask_restful import Resource
from flask import request

paciente_schema = PacienteSchema()

class VistaRegistrarPaciente(Resource):
    
    def post(self):
        nuevo_paciente = Paciente(
            nombre=request.json['nombre'],\
            apellido=request.json['apellido'])
        db.session.add(nuevo_paciente)
        db.session.commit()
        return paciente_schema.dump(nuevo_paciente)

    def get(self):
        return [paciente_schema.dump(ca) for ca in Paciente.query.all()]