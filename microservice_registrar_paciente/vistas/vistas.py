from microservice_registrar_paciente.modelos.modelos import HistoriaClinicaSchema, Registro, db, Paciente, PacienteSchema, HistoriaClinica
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError

paciente_schema = PacienteSchema()
historia_clinica_schema = HistoriaClinicaSchema()

class VistaPaciente(Resource):
    
    def post(self):
        nuevo_paciente = Paciente(
            nombre=request.json['nombre'],
            apellido=request.json['apellido'])

        nueva_historia_clinica = HistoriaClinica()
        nuevo_paciente.historia_clinica=nueva_historia_clinica

        db.session.add(nuevo_paciente)
        db.session.commit()
        return paciente_schema.dump(nuevo_paciente)

    def get(self):
        return [paciente_schema.dump(ca) for ca in Paciente.query.all()]

    
class VistaHistoriaClinicaPaciente(Resource):

    def get(self, id_paciente):
        paciente = Paciente.query.get_or_404(id_paciente)
        info_historia_clinica = historia_clinica_schema.dump(paciente.historia_clinica)
        return info_historia_clinica

class VistaRegistroHistoriaClinica(Resource):

    def post(self, id_historia_clinica):
        historia_clinica = HistoriaClinica.query.get_or_404(id_historia_clinica)
        nuevo_registro = Registro(informacion=request.json["informacion"])
        historia_clinica.registros.append(nuevo_registro)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'No se pudo registrar la historia clínica del paciente', 409
        
        return historia_clinica_schema.dump(historia_clinica)

