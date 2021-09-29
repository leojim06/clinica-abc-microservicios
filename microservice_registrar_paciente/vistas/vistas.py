from ..modelos import db, Paciente, PacienteSchema
from flask_restful import Resource
from flask import request
import hmac
import hashlib
import base64
import json

paciente_schema = PacienteSchema()

class VistaRegistrarPaciente(Resource):
    
    def post(self):
        print(request.json)
        nuevo_paciente = Paciente(
            nombre=request.json['nombre'],
            apellido=request.json['apellido'])

        httpsig = request.headers.get('Httpsig')
        computed_Digest = request.headers.get('Computed-Digest')
        current_Date = request.headers.get('Current-Date')
        target_Url = request.headers.get('Target-Url')

        a1 = dict(item.split('=',1) for item in httpsig.split(','))
        signature = a1['signature'].replace('"', '')
        hash_body = VistaRegistrarPaciente.calcular_hash_body(request.json)
        signature_calculated = VistaRegistrarPaciente.calcular_signature(target_Url, current_Date, hash_body)

        if signature == signature_calculated:
            return {}, 200
        return {}, 400
        # db.session.add(nuevo_paciente)
        # db.session.commit()
        # return paciente_schema.dump(nuevo_paciente)

    def get(self):
        return [paciente_schema.dump(ca) for ca in Paciente.query.all()]


    def calcular_signature(target_url, date, digest):
        cadena = "(request-target): {target_url}\ndate: {date}\ndigest: {digest}".format(target_url=target_url, date=date, digest=digest)
        hmacsha256 = hmac.new(key=bytes("abcdefghijk", 'latin-1'), msg=cadena.encode(), digestmod=hashlib.sha256).digest()
        hmacbase64 = base64.b64encode(hmacsha256)
        return hmacbase64.decode('utf-8')

    def calcular_hash_body(body):
        s = json.dumps(body, separators=(',', ':'))
        result = base64.b64encode(hashlib.sha256(s.encode()).digest())
        return result.decode('utf-8')