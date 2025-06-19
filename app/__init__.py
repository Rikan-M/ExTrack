from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect



db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="7h15_1s_3y_5uper_6ret_key"
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///expanceTracker.db"
    app.config["SQLALCHEMY_TRACKS_MODIFICATION"]=False
    db.init_app(app)
    csrf = CSRFProtect(app)
    from app.routes.auth import auth_bp
    from app.routes.content import cont_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(cont_bp)
    return app