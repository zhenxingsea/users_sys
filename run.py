from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

app = create_app("config")
jwt = JWTManager(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)

@jwt.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    return jwt_data["sub"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
