from flaskr.modelos.modelos import db, UsuarioSchema, Usuario, Rol
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from flask import request

usuario_schema = UsuarioSchema()

class VistaAutorizador(Resource):
    
    @jwt_required()
    def post(self):

        rutas_superusuario = ['historia-clinica', 'registro']
        rutas_lectura = ['historia-clinica']

        target_Url = request.headers.get('Target-Url')
        print(target_Url)
        target_route = target_Url.split('/')[-1:][0]
        print(target_route)

        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(usuario_id)
        print(usuario.rol)

        if usuario.rol == Rol.BASICO:
            return {}, 403

        if usuario.rol == Rol.LECTURA:
            ruta = (list(filter(lambda x: target_route in x, rutas_lectura))[:1] or [None])[0]
            print(ruta)
            if ruta is None or ruta != target_route:
                return {}, 403

        if usuario.rol == Rol.SUPERADMIN:
            ruta = (list(filter(lambda x: target_route in x, rutas_superusuario))[:1] or [None])[0]
            print(ruta)
            if ruta is None or ruta != target_route:
                return {}, 403

        return {}, 200

class VistaLogIn(Resource):
    
    def post(self):
        usuario = Usuario.query.filter_by(nombre=request.json["nombre"], contrasena=request.json["contrasena"]).first()
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