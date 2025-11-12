from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms.auth import RegistrationForm, LoginForm
from forms.m03_student import StudentForm, TuitionForm
from logic import register_user, login_user
from logic.auth import auth_bp
from logic.m02_user import profile_bp
from logic.m03_student import student_bp 
from logic.m04_course import course_bp
from config import Config
from extensions import db, migrate, login_manager 
from models import *
from flask_login import login_required, current_user
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(student_bp)
app.register_blueprint(course_bp)
db.init_app(app)
migrate.init_app(app, db)

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_key=ON')
        cursor.close()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile')
@login_required
def profile():
    return render_template('m02_user.html', user=current_user)


@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        return {
            'current_user_first_name': current_user.first_name,
            'current_user_last_name': current_user.last_name,
            'current_user_email': current_user.email
        }
    return {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()