from flask_restful import Resource
from flask import jsonify
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from Model import *
import uuid
from datetime import datetime, timedelta


class AuthApplications(Resource):
    def get(self):
        return ""

    @jwt_required()
    def post(self):
        name = request.json.get("name", None)
        server = request.json.get("server", None)
        password = request.json.get("password", None)
        secret_key = request.json.get("secret_key", None)
        reslut = {}
        if name and server and password and secret_key:
            try:
                id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.now())))
                sysuid = current_user['uid']
                print(sysuid)
                create_time = datetime.now()
                update_time = datetime.now()
                validity_time = datetime.now() + timedelta(days=360)
                authApplication = AuthApplicationsModel(id=id, name=name, sysuid=sysuid, secret_key=secret_key,
                                                        create_time=create_time, update_time=update_time,
                                                        validity_time=validity_time, server=server,
                                                        is_auth=1)
                db.session.add(authApplication)
                db.session.commit()
                reslut["code"] = 200
                reslut["message"] = "register authApplication succeed"
            except Exception as err:
                db.session.rollback()
                reslut["code"] = 200
                reslut["message"] = "register authApplication fail"
        else:
            reslut["code"] = 400
            reslut["message"] = "parameter non-compliance"
        return jsonify(reslut)
