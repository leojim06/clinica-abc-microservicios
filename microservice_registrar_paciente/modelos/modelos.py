from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    apellido = db.Column(db.String(128))

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        load_instance = True
