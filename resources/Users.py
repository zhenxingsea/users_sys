from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from flask import jsonify
from Model import *
from datetime import datetime


class Users(Resource):
    @jwt_required()
    def get(self):
        return "fgdgfdsgfd"

    @jwt_required()
    def post(self):
        username = request.json.get("username", None)
        password1 = request.json.get("password1", None)
        password2 = request.json.get("password2", None)
        device_id = request.json.get("device_id", None)
        secret_key = request.json.get("secret_key", None)
        application_id = request.json.get("application_id", None)
        if password1 is not None and password2 is not None and username is not None:
            sysuser = SysUsersModel(uid="dfd", name=username, password=password1, device_id=device_id,
                               secret_key=secret_key, application_id=application_id,
                               create_time=datetime.now(), update_time=datetime.now(),
                               validity_time=datetime.now())
            db.session.add(sysuser)
            db.session.commit()
            return jsonify(code=200, message="注册成功")
        else:
            return jsonify(code=500, message="注册失败")
