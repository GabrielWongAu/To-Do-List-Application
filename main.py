from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate  
from flask.cli import with_appcontext

db = SQLAlchemy()
mar = Marshmallow()
bcrypt = Bcrypt()
# jwt = JWTManager()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate() 

def create_app():
    app = Flask(__name__)
    app.config.from_object("default_settings.app_config")

    db.init_app(app)
    mar.init_app(app)
    bcrypt.init_app(app)
    # jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    from models.User import get_user

    @login_manager.user_loader
    def load_user(user_id):
        return get_user(user_id)

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    # from commands import create_tables
    # app.cli.add_command(create_tables)
    
    with app.app_context():
        db.create_all()

    return app