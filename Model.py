from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class SysUsers(db.Model):
    __tablename__ = 'sysusers'
    uid = db.Column(db.String(20), primary_key=True, unique=True)
    name = db.Column(db.String(30), unique=True)
    device_id = db.Column(db.String(64), unique=True)
    secret_key = db.Column(db.String(255), unique=True)
    application_id = db.Column(db.String(10), unique=True)
    create_time = db.Column(db.DateTime, unique=True)
    update_time = db.Column(db.DateTime, unique=True)
    validity_time = db.Column(db.DateTime, unique=True)

    def __init__(self, uid, name, device_id, secret_key, application_id, create_time, update_time, validity_time):
        self.uid = uid
        self.name = name
        self.device_id = device_id
        self.secret_key = secret_key
        self.application_id = application_id
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time


class Users(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.String(20), primary_key=True, unique=True)
    name = db.Column(db.String(30), unique=True)
    source = db.Column(db.String(128), unique=True)
    device_id = db.Column(db.String(64), unique=True)
    secret_key = db.Column(db.String(255), unique=True)
    application_id = db.Column(db.String(10), unique=True)
    create_time = db.Column(db.DateTime, unique=True)
    update_time = db.Column(db.DateTime, unique=True)
    validity_time = db.Column(db.DateTime, unique=True)

    def __init__(self, uid, name, source, device_id, secret_key, application_id, create_time, update_time,
                 validity_time):
        self.uid = uid
        self.name = name
        self.source = source
        self.device_id = device_id
        self.secret_key = secret_key
        self.application_id = application_id
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time


class Applications(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.String(10), primary_key=True, unique=True)
    name = db.Column(db.String(30), unique=True)
    device_id = db.Column(db.String(64), unique=True)
    secret_key = db.Column(db.String(255), unique=True)
    create_time = db.Column(db.DateTime, unique=True)
    update_time = db.Column(db.DateTime, unique=True)
    validity_time = db.Column(db.DateTime, unique=True)

    def __init__(self, id, name, device_id, secret_key, create_time, update_time, validity_time):
        self.id = id
        self.name = name
        self.device_id = device_id
        self.secret_key = secret_key
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time


class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.String(64), primary_key=True, unique=True)
    system = db.Column(db.String(20), unique=True)
    platform = db.Column(db.String(20), unique=True)
    application = db.Column(db.String(30), unique=True)
    create_time = db.Column(db.DateTime, unique=True)
    update_time = db.Column(db.DateTime, unique=True)
    validity_time = db.Column(db.DateTime, unique=True)

    def __init__(self, id, system, platform, application, create_time, update_time, validity_time):
        self.id = id
        self.system = system
        self.platform = platform
        self.application = application
        self.create_time = create_time
        self.update_time = update_time
        self.validity_time = validity_time
