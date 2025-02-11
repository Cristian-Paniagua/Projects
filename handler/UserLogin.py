from flask import jsonify
from dao.DaoUserLogin import UserLoginDao

class UserHandler:

    def validateLogin(self, username, password):
        if not username or not password:
            return {"error": "Username and password are required"}, 400
        return None

    def register_user(self, username, password):
        dao = UserLoginDao()
        dao.create_user(username, password)

    def login(self, login):
        username = login.get('username')
        password = login.get('password')
        dao = UserLoginDao()


        validation_error = self.validateLogin(username, password)
        if validation_error:
            return jsonify(validation_error)

        user = dao.getUserByUsername(username)
        if user:
            stored_password = user[2]
            if password == stored_password:
                response = {
                    "uid": user[0],
                    "username": user[1]
                }
                return jsonify(response), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 401
        else:
            return jsonify({"error": "Invalid username or password"}), 401
