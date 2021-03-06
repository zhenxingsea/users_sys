from flask import Blueprint
from flask_restful import Api
from resources.SysUsers import SysUsers
from resources.Users import Users
from resources.Devices import Devices
from resources.AuthApplications import AuthApplications
from resources.Login import Login
from resources.AuthUsers import AuthUsers

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(SysUsers, '/SysUsers')
api.add_resource(Devices, '/Devices')
api.add_resource(AuthApplications, '/AuthApplications')
api.add_resource(Login, '/Login')
api.add_resource(AuthUsers, '/AuthUsers')

