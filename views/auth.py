from flask import request
from flask_restx import Resource, Namespace

from implemented import user_service


auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        data = request.json
        if data.get('username') and data.get('password'):
            return user_service.check(data.get('username'), data.get('password')), 201
        else:
            return 'Something wrong', 401

    def put(self):
        data = request.json
        if data.get('refresh_token'):
            return user_service.update_token(data.get('refresh_token')), 201
        else:
            return 'Something wrong', 401
