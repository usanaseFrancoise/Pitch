from flask import Flask
from config import config_options
from flask_mail import Mail
from flask_login import LoginManager
# from flask_bootstarp import Bootstarp
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES,UploadSet,configure_uploads
from flask_simplemde import SimpleMDE
db=SQLAlchemy()
mail=Mail()
bootstrap=Bootstrap()
simple=SimpleMDE()

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
photos=UploadSet('photos',IMAGES)

def create_app(config_name):
    app=Flask(__name__)

    app.config.from_object(config_options[config_name])
    from .auth import auth as authentication_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(authentication_blueprint,url_prefix='/authenticate')
    app.register_blueprint(main_blueprint)

    login_manager.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    configure_uploads(app,photos)
    mail.init_app(app)
    # simple.init_app(app)
    
    return app



