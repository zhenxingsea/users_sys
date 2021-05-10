from flask import Flask

app = Flask(__name__)
app.config.from_object("config")

if __name__ == "__main__":
    from Model import *
    from Auth import *
    from views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    # db.drop_all()
    # db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)
