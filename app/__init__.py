from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))