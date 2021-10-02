from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))



class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    apellido = db.Column(db.String(128))

class PacienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Paciente
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True