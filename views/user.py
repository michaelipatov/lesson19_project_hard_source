from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        query = user_service.get_all()
        queries = UserSchema(many=True).dump(query)
        return queries, 200

    def post(self):
        data = request.json
        if data.get('username') and data.get('password') and data.get('role'):
            return user_service.create(data.get('username'), data.get('password'), data.get('role')), 201
        else:
            return 'Something wrong', 401


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        query = user_service.get_one(uid)
        queries = UserSchema().dump(query)
        return queries, 200

    def put(self, mid: int):
        data = request.json
        data["id"] = mid

        if data.get('username') and data.get('password') and data.get('role'):
            return user_service.update(data), 201
        else:
            return 'Something wrong', 401

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
