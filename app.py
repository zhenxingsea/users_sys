from flask import Blueprint
from flask_restful import Api
from resources.SysUsers import SysUsers
from resources.Users import Users
from resources.Devices import Devices
from resources.Applications import Applications
from resources.Login import Login

# from resources.Category import CategoryResource
# from resources.Comment import CommentResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(SysUsers, '/SysUsers')
api.add_resource(Users, '/Users')
api.add_resource(Devices, '/Devices')
api.add_resource(Applications, '/Applications')
api.add_resource(Login, '/Login')
