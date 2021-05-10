from flask_restful import Resource
from flask import jsonify
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from Model import *
import uuid
from datetime import datetime, timedelta


class AuthApplications(Resource):
    @jwt_required()
    def get(self):
        get_type = request.args.get("get_type", "all")
        page = request.args.get("page", 0)
        limit = request.args.get("limit", 10)
        name = request.args.get("name", "")
        result = {"code": 500, "message": "get fail"}
        if get_type == "count":
            count = AuthApplicationsModel.query.count()
            result["count"] = count
            result["code"] = 200
            result["message"] = "get succeed"
        if get_type == "all":
            authApplications = AuthApplicationsModel.query.limit(int(limit)).offset(int(page) * int(limit)).order_by(
                AuthApplicationsModel.create_time.desc()).all()
            count = AuthApplicationsModel.query.count()
            result["count"] = count
            result["code"] = 200
            result["message"] = "get succeed"
            result["data"] = []
            result["current_page"] = int(page)
            for aa in authApplications:
                aas = AuthApplicationSchema()
                aaj = aas.dump(aa)
                result["data"].append(aaj)
        if get_type == "name":
            authApplications = AuthApplicationsModel.query.filter(
                AuthApplicationsModel.name.contains(name, autoescape=True)).order_by(
                AuthApplicationsModel.create_time.desc()).limit(
                int(limit)).offset(int(page) * int(limit)).all()
            count = AuthApplicationsModel.query.filter(
                AuthApplicationsModel.name.contains(name, autoescape=True)).count()
            result["count"] = count
            result["data"] = []
            result["code"] = 200
            result["message"] = "get succeed"
            result["current_page"] = int(page)
            for aa in authApplications:
                aas = AuthApplicationSchema()
                aaj = aas.dump(aa)
                result["data"].append(aaj)
        return jsonify(result)

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
