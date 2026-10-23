from flask import Flask
from flask_login import LoginManager
from .models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-later'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # THIS IS STEP 4: Import and register the auth blueprint
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    with app.app_context():
        db.create_all()
        
    return app