from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    links = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(1), nullable=True)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, input_password):
        return check_password_hash(self.password_hash, input_password)
    

    def __init__(self, email, name=None, phone=None, raw_password=None):
        self.email = email
        self.phone = phone
        if raw_password:
            self.set_password(raw_password)
       

    def __repr__(self):
        return f'<User {self.name}, {self.email}, {self.phone}>'