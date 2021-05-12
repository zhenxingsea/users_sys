from marshmallow import Schema, fields, pre_load, validate
from sqlalchemy import and_
from app import app
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class SysUsersModel(db.Model):
    __tablename__ = 'sys_users'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    secret_key = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    validity_time = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    is_auth = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, uid, name, password, secret_key, create_time, update_time, validity_time, last_login, is_auth):
        self.uid = uid
        self.name = name
        self.password = password
        self.secret_key = secret_key
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
        self.last_login = last_login
        self.is_auth = is_auth


class SysUserSchema(ma.Schema):
    uid = fields.String()
    name = fields.String()
    password = fields.String()
    secret_key = fields.String()
    create_time = fields.DateTime(format=DATETIME_FORMAT)
    update_time = fields.DateTime(format=DATETIME_FORMAT)
    validity_time = fields.DateTime(format=DATETIME_FORMAT)
    last_login = fields.DateTime(format=DATETIME_FORMAT)
    is_auth = fields.Number()

    class Meta:
        fields = ["uid", "name", "password", "secret_key", "create_time", "update_time",
                  "validity_time", "last_login", "is_auth"]
        ordered = True


class AuthUsersModel(db.Model):
    __tablename__ = 'auth_users'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    source = db.Column(db.String(128), nullable=False)
    secret_key = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    validity_time = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

    def __init__(self, uid, name, password, source, secret_key, create_time, update_time,
                 validity_time, last_login):
        self.uid = uid
        self.name = name
        self.password = password
        self.source = source
        self.secret_key = secret_key
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
        self.last_login = last_login


class AuthUsersSchema(ma.Schema):
    uid = fields.String()
    name = fields.String()
    password = fields.String()
    source = fields.String()
    secret_key = fields.String()
    create_time = fields.DateTime(format=DATETIME_FORMAT)
    update_time = fields.DateTime(format=DATETIME_FORMAT)
    validity_time = fields.DateTime(format=DATETIME_FORMAT)
    last_login = fields.DateTime(format=DATETIME_FORMAT)

    class Meta:
        fields = ["uid", "name", "password", "secret_key", "create_time", "update_time",
                  "validity_time", "last_login"]
        ordered = True


class ApplicationsModel(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    uid = db.Column(db.String(36), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    validity_time = db.Column(db.DateTime, nullable=False)
    is_auth = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, id, name, uid, create_time, update_time, validity_time, is_auth):
        self.id = id
        self.name = name
        self.uid = uid
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
        self.is_auth = is_auth


class ApplicationSchema(ma.Schema):
    id = fields.String()
    name = fields.String()
    uid = fields.String()
    create_time = fields.DateTime(format=DATETIME_FORMAT)
    update_time = fields.DateTime(format=DATETIME_FORMAT)
    validity_time = fields.DateTime(format=DATETIME_FORMAT)
    is_auth = fields.Number()

    class Meta:
        fields = ["id", "name", "uid", "create_time", "update_time",
                  "validity_time", "is_auth"]
        ordered = True


class AuthApplicationsModel(db.Model):
    __tablename__ = 'auth_applications'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    sysuid = db.Column(db.String(36), nullable=False)
    server = db.Column(db.String(64), nullable=False)
    secret_key = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    validity_time = db.Column(db.DateTime, nullable=False)
    is_auth = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, id, name, sysuid, secret_key, create_time, update_time, validity_time, server, is_auth):
        self.id = id
        self.name = name
        self.sysuid = sysuid
        self.secret_key = secret_key
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
        self.is_auth = is_auth
        self.server = server


class AuthApplicationSchema(ma.Schema):
    id = fields.String()
    name = fields.String()
    sysuid = fields.String()
    secret_key = fields.String()
    create_time = fields.DateTime(format=DATETIME_FORMAT)
    update_time = fields.DateTime(format=DATETIME_FORMAT)
    validity_time = fields.DateTime(format=DATETIME_FORMAT)
    is_auth = fields.Number()
    server = fields.String()

    class Meta:
        fields = ["id", "name", "sysuid", "secret_key", "create_time", "update_time",
                  "validity_time", "is_auth", "server"]
        ordered = True


class DevicesModel(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.String(64), primary_key=True)
    uid = db.Column(db.String(36), nullable=False)
    system = db.Column(db.String(20), nullable=False)
    platform = db.Column(db.String(20), nullable=False)
    application = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    validity_time = db.Column(db.DateTime, nullable=False)
    is_auth = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, id, uid, system, platform, application, create_time, update_time, validity_time, is_auth):
        self.id = id
        self.uid = uid
        self.system = system
        self.platform = platform
        self.application = application
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
        self.is_auth = is_auth


class DeviceSchema(ma.Schema):
    id = fields.String()
    uid = fields.String()
    system = fields.String()
    platform = fields.String()
    application = fields.String()
    create_time = fields.DateTime(format=DATETIME_FORMAT)
    update_time = fields.DateTime(format=DATETIME_FORMAT)
    validity_time = fields.DateTime(format=DATETIME_FORMAT)
    is_auth = fields.Number()

    class Meta:
        fields = ["id", "uid", "system", "platform", "create_time", "update_time", "application",
                  "validity_time", "is_auth"]
        ordered = True


class AuthUsersAuthApplications(db.Model):
    __tablename__ = 'auth_users_auth_applications'
    auid = db.Column(db.String(36), primary_key=True)
    aaid = db.Column(db.String(64), primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    validity_time = db.Column(db.DateTime, nullable=False)
    is_auth = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, auid, aaid, create_time, update_time, validity_time, is_auth):
        self.auid = auid
        self.aaid = aaid
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
        self.is_auth = is_auth
