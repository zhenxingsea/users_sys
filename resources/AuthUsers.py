from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from flask import jsonify
from Model import *
from datetime import datetime, timedelta
import re
import uuid
import hashlib


def password_level(password):
    weak = re.compile(r'^((\d+)|([A-Za-z]+)|(\W+))$')
    level_weak = weak.match(password)
    level_middle = re.match(r'([0-9]+(\W+|\_+|[A-Za-z]+))+|([A-Za-z]+(\W+|\_+|\d+))+|((\W+|\_+)+(\d+|\w+))+', password)
    level_strong = re.match(r'(\w+|\W+)+', password)
    if level_weak:
        # print('password level is weak', level_weak.group())
        return 1
    else:
        if (level_middle and len(level_middle.group()) == len(password)):
            # print('password level is weak', level_weak.group())
            return 2
        else:
            if level_strong and len(level_strong.group()) == len(password):
                # print('password level is strong', level_strong.group())
                return 3
        return 0


class AuthUsers(Resource):
    @jwt_required()
    def get(self):
        return "fgdgfdsgfd"

    def post(self):
        auth_type = request.json.get("auth_type", None)
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        password1 = request.json.get("password1", None)
        password2 = request.json.get("password2", None)
        device_id = request.json.get("device_id", None)
        application_id = request.json.get("application_id", None)
        application_name = request.json.get("application_name", None)
        code = request.json.get("code", None)
        source = request.json.get("source", None)
        secret_key = request.json.get("secret_key", None)
        system = request.json.get("system", None)
        platform = request.json.get("platform", None)
        result = {}
        if auth_type == "password":
            if password and username:
                result = self.auth_password(username, password, device_id, application_id, result)
            else:
                result["code"] = 200
                result["message"] = "password or user non-compliance"
        elif auth_type == "code":
            result = self.auth_code(code, device_id, application_id, result)
        elif auth_type == "message":
            result = self.message_auth()
        elif auth_type == "face":
            result = self.face_auth()
            return jsonify(result)
        elif auth_type == "register":
            result = self.user_register(username, password1, password2, source, device_id, application_id,
                                        application_name,
                                        secret_key, system, platform, result)
            return jsonify(result)
        else:
            result = {"code": 500, "message": "auth type non-compliance"}
        return jsonify(result)

    def auth_password(self, username, password, device_id, application_id, result):
        pw = hashlib.new("sha256")
        pw.update(password.encode("utf-8"))
        password = pw.hexdigest()
        authuser = AuthUsersModel.query.filter(and_(
            AuthUsersModel.name == username, AuthUsersModel.password == password)).first()
        if authuser:
            application = ApplicationsModel.query.filter(
                and_(ApplicationsModel.id == application_id, ApplicationsModel.uid == authuser.uid)).first()
            if application and application.validity_time > datetime.now() and application.is_auth == 1:
                device = DevicesModel.query.filter(
                    and_(DevicesModel.id == device_id, DevicesModel.uid == authuser.uid)).first()
                if device and device.validity_time > datetime.now() and device.is_auth == 1:
                    authuser.last_login = datetime.now()
                    application.validity_time += timedelta(days=7)
                    device.validity_time += timedelta(days=7)
                    db.session.commit()
                    result["code"] = 200
                    result["message"] = "auth succeed"
                else:
                    result["code"] = 402
                    result["message"] = "device non-compliance"
            else:
                result["code"] = 401
                result["message"] = "application non-compliance"
        else:
            result["code"] = 400
            result["message"] = "password or user non-compliance"
        return result

    def auth_code(self, code, device_id, application_id, result):
        pass

    def message_auth(self):
        pass

    def face_auth(self):
        pass

    def user_register(self, username, password1, password2, source, device_id, application_id, application_name,
                      secret_key, system, platform, result):
        if username is None:
            result["code"] = 300
            result["message"] = "username is null"
            return result
        if password1 is None or password2 is None:
            result["code"] = 300
            result["message"] = "password is null"
            return result
        if password2 != password1:
            result["code"] = 300
            result["message"] = "password1 different password2"
            return result
        if password_level(password1) < 2:
            result["code"] = 300
            result["message"] = "password non-compliance"
            return result
        if source is None:
            result["code"] = 300
            result["message"] = "source is null"
        if device_id is None:
            result["code"] = 300
            result["message"] = "device_id is null"
        if application_id is None:
            result["code"] = 300
            result["message"] = "application_id is null"
        try:
            uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))
            application = ApplicationsModel(id=application_id, name=application_name, uid=uid,
                                            create_time=datetime.now(),
                                            update_time=datetime.now(),
                                            validity_time=datetime.now() + timedelta(days=360),
                                            is_auth=1)
            device = DevicesModel(id=device_id, uid=uid, system=system, platform=platform, application=application_name,
                                  create_time=datetime.now(), update_time=datetime.now(),
                                  validity_time=datetime.now() + timedelta(days=360),
                                  is_auth=1)
            password = hashlib.new("sha256")
            password.update(password1.encode("utf-8"))
            password = password.hexdigest()
            authuser = AuthUsersModel(uid=uid, name=username, password=password, source=source, secret_key=secret_key,
                                      create_time=datetime.now(), update_time=datetime.now(),
                                      validity_time=datetime.now() + timedelta(days=360), last_login=datetime.now())
            db.session.add(application)
            db.session.add(device)
            db.session.add(authuser)
            db.session.commit()
            result["code"] = 200
            result["message"] = "register succeed"
        except Exception as err:
            err.with_traceback()
            db.session.rollback()
            result["code"] = 500
            result["message"] = "register fail"
        return result
