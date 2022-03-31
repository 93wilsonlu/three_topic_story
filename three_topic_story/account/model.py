from .. import db, bcrypt, login
from flask_jwt_extended import create_access_token, decode_token
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    confirm = db.Column(db.Boolean, default=False)

    about_me = db.Column(db.Text())
    regist_date = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User id:{self.id}, username:{self.username}, email:{self.email}>'

    def create_confirm_token(self):
        return create_access_token(identity={'user_id': self.id})

    def create_reset_token(self):
        return create_access_token(identity={'reset_id': self.id})

    def validate_confirm_token(self, token):
        try:
            data = decode_token(token)
        except:
            return False
        return data['sub']


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
