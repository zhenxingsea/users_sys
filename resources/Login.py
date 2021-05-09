from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from flask import jsonify
from Model import *

class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if self.auth(username, password):
            access_token = create_access_token(identity={"username": username, "uid": 1})
            return jsonify(access_token=access_token)
        else:
            return {}

    def auth(self, username, password):
        return True
