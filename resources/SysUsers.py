from flask_restful import Resource
from flask import request
from flask import jsonify
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from Model import *
import uuid
from datetime import datetime, timedelta


class SysUsers(Resource):
    @jwt_required()
    def get(self):
        get_type = request.args.get("get_type", "me")
        result = {}
        if get_type == "me":
            uid = current_user['uid']
            sysuser = SysUsersModel.query.filter(SysUsersModel.uid==uid).first()
            sysUserSchema = SysUserSchema()
            jSysUserSchema = sysUserSchema.dump(sysuser)
            result["code"] = 200
            result["data"] = jSysUserSchema
            result["message"] = "get user info succeed"

        return jsonify(result)

    def post(self):
        username = request.json.get("username", None)
        password1 = request.json.get("password1", None)
        password2 = request.json.get("password2", None)
        result = {}
        if username and password1 and password2:
            if password2 == password1:
                try:
                    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.now())))
                    sysUser = SysUsersModel(uid=uid, name=username, password=password1, secret_key=None,
                                            create_time=datetime.now(), update_time=datetime.now(),
                                            validity_time=datetime.now() + timedelta(days=360), last_login=datetime.now(),
                                            is_auth=0)
                    db.session.add(sysUser)
                    db.session.commit()
                    result["code"] = 200
                    result["message"] = "register succeed"
                except Exception as err:
                    # err.with_traceback()
                    db.session.rollback()
                    result["code"] = 500
                    result["message"] = "register err"
            else:
                result["code"] = 401
                result["message"] = "password1 != password2"
        else:
            result["code"] = 400
            result["message"] = "parameter non-compliance"
        return jsonify(result)
