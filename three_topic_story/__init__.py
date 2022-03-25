from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from .config import Config

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config.from_object(Config)

# import all app
from three_topic_story.main import main_blueprint
app.register_blueprint(main_blueprint)
