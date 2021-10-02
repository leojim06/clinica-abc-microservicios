from flask_restful import Resource
from flask import request
import hashlib



class VistaGenerarHash(Resource):
    def post(self):
        texto = request.json["texto"]
        textoMD5 = hashlib.md5()
        textoMD5.update(texto.encode("UTF-8"))
        textoMD5 = textoMD5.hexdigest()
        return textoMD5

