from flask_restful import Resource
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

class Users(Resource):
    @jwt_required()
    def get(self):
        print(current_user)
        return "fgdgfdsgfd"

    def post(self):
        return {"message": "Hello, World!"}