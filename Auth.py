from flask_jwt_extended import JWTManager
from app import app

jwt = JWTManager(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    return jwt_data["sub"]
