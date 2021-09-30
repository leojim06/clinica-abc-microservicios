import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields

db = SQLAlchemy()

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    apellido = db.Column(db.String(128))
    historia_clinica = db.relationship('HistoriaClinica', uselist=False, backref='paciente')

class HistoriaClinica(db.Model):
    __tablename__ = 'historias_clinicas'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    registros = db.relationship('Registro', backref='HistoriaClinica', cascade='all, delete, delete-orphan')

class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    informacion = db.Column(db.String(128))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    historia_clinica_id = db.Column(db.Integer, db.ForeignKey("historias_clinicas.id"))



class RegistroSchema(Schema):
    id = fields.Integer()
    informacion = fields.String()
    fecha_creacion = fields.DateTime()
    # historia_clinica_id = fields.Integer()

class HistoriaClinicaSchema(Schema):
    id = fields.Integer()
    paciente_id = fields.Integer()
    fecha_creacion = fields.DateTime()
    registros = fields.List(fields.Nested(RegistroSchema))

class PacienteSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()
    apellido = fields.String()
    historia_clinica = fields.Nested(HistoriaClinicaSchema)