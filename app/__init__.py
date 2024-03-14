from flask import Flask, url_for
from .extensions import db, migrate, scheduler
from flask_login import LoginManager



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pLoHwegfhioAW243hiofkwJHb5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    # Creates cookie for the user see: https://www.youtube.com/watch?v=K0vSCCAM2ss
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .dpow import dpow as dpow_blueprint
    app.register_blueprint(dpow_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    migrate.init_app(app, db)
    

    


    return app