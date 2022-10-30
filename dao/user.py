from dao.model.user import User
from service.tools.security import generate_password_hash


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_login(self, username):
        try:
            stmt = self.session.query(User).filter(User.username == username).one()
            return stmt
        except Exception as e:
            print(e)
            return {}

    def create(self, username, password, role):
        try:
            self.session.add(
                User(
                    username=username,
                    password=generate_password_hash(password),
                    role=role
                ))
            self.session.commit()
            print('Пользователь добавлен')
        except Exception as e:
            print(e)
            self.session.rollback()

    def update(self, data):
        try:
            self.session.query(User).update(data)
            self.session.commit()
            print("Пользователь обновлен")
        except Exception as e:
            print(e)
            self.session.rollback()

    def delete(self, rid):
        director = self.get_one(rid)
        self.session.delete(director)
        self.session.commit()
