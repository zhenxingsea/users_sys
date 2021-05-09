from flask_restful import Resource
from flask import request

class SysUsers(Resource):
    def get(self):
        return ""

    def post(self):
        return {"message": "Hello, World!"}
