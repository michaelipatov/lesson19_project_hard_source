from dao.user import UserDAO
from service.tools.security import generate_tokens, approve_refresh_token


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, username, password, role):
        return self.dao.create(username, password, role)

    def update(self, data):
        uid = data.get("id")
        user = self.get_one(uid)

        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")

        self.dao.update(data)

    def delete(self, rid):
        self.dao.delete(rid)

    def get_user_by_login(self, username):
        return self.dao.get_user_by_login(username)

    def check(self, username, password):
        user = self.get_user_by_login(username)
        return generate_tokens(username=user.username, password=password, password_hash=user.password)

    def update_token(self, refresh_token):
        return approve_refresh_token(refresh_token)
