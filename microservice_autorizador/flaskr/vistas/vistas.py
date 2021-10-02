from flaskr.modelos.modelos import db, UsuarioSchema, Usuario
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from flask import request

usuario_schema = UsuarioSchema()

class VistaLogIn(Resource):
    
    def post(self):
        usuario = Usuario.query.filter_by(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}

class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"], rol=request.json["rol"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {'mensaje ': 'Usuario creado exitosamente', 'token' : token_de_acceso}

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