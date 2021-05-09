from flask_restful import Resource
from flask import request

class Users(Resource):
    def get(self):
        return ""

    def post(self):
        return {"message": "Hello, World!"}