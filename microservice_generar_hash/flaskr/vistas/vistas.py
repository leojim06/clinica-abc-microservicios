from flask_restful import Resource
from flask import request
import hashlib
import base64
import hmac
import json


class VistaGenerarHash(Resource):
    
    def post(self):

        httpsig = request.headers.get('Httpsig')
        current_Date = request.headers.get('Current-Date')
        target_Url = request.headers.get('Target-Url')
        a1 = dict(item.split('=',1) for item in httpsig.split(','))
        signature = a1['signature'].replace('"', '')
        hash_body = VistaGenerarHash.calcular_hash_body(request.json)
        signature_calculated = VistaGenerarHash.calcular_signature(target_Url, current_Date, hash_body)
        
        if signature == signature_calculated:
            return {}, 200
        
        return {}, 400

    def calcular_signature(target_url, date, digest):
        cadena = "(request-target): {target_url}\ndate: {date}\ndigest: {digest}".format(target_url=target_url, date=date, digest=digest)
        hmacsha256 = hmac.new(key=bytes("abcdefghijk", 'latin-1'), msg=cadena.encode(), digestmod=hashlib.sha256).digest()
        hmacbase64 = base64.b64encode(hmacsha256)
        return hmacbase64.decode('utf-8')

    def calcular_hash_body(body):
        s = json.dumps(body, separators=(',', ':'))
        result = base64.b64encode(hashlib.sha256(s.encode()).digest())
        return result.decode('utf-8')

