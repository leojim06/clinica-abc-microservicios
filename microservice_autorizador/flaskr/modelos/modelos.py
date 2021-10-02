from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

class Rol(enum.Enum):
   BASICO = 1
   LECTURA = 2
   SUPERADMIN = 3

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    rol = db.Column(db.Enum(Rol))


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class UsuarioSchema(SQLAlchemyAutoSchema):
    rol = EnumADiccionario(attribute=("rol"))
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True