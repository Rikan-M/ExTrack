from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os


db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
 
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
    csrf = CSRFProtect(app)
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///.ExpTracker.db"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300 
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.content import cont_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(cont_bp)
    
    return app