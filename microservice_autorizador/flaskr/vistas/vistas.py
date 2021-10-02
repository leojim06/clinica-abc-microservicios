from ..modelos import db, Paciente, PacienteSchema, UsuarioSchema, Usuario
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token

paciente_schema = PacienteSchema()
usuario_schema = UsuarioSchema()


class VistaRegistrarPaciente(Resource):
    @jwt_required()
    def post(self):
        nuevo_paciente = Paciente(
            nombre=request.json['nombre'],\
            apellido=request.json['apellido'])
        db.session.add(nuevo_paciente)
        db.session.commit()
        return paciente_schema.dump(nuevo_paciente)


class VistaLogIn(Resource):
    def post(self):
        u_nombre = request.json["nombre"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena=u_contrasena).all()
        if usuario:
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        token_de_acceso = create_access_token(identity=request.json['nombre'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'mensaje ': 'Usuario creado exitosamente', 'token_de_acceso' : token_de_acceso}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204