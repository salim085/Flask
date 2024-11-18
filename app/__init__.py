import secrets
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
SECRET_KEY = "my_super_secret_key_1234567890_!@#$%^&*"
DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
load_dotenv()
def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.controllers.user_controller import user_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.property_controller import property_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(property_bp)

    return app
