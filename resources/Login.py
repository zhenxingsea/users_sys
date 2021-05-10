from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from flask import jsonify
from Model import *


class Login(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        sysuser = self.auth(username, password)
        if sysuser:
            access_token = create_access_token(identity={"username": sysuser["name"], "uid": sysuser["uid"]})
            return jsonify(code=200, message="login succeed", access_token="Bearer " + access_token)
        else:
            return jsonify(code=401, message="login fail")

    def auth(self, username, password):
        sysuser = SysUsersModel.query.filter_by(name=username, password=password).first()
        if sysuser:
            sysuser = SysUserSchema().dump(sysuser)
            return sysuser
        else:
            return False
