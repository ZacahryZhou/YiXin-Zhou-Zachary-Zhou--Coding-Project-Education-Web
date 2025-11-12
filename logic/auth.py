from models.user import User
from forms import RegistrationForm, LoginForm
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user
auth_bp = Blueprint('auth', __name__)

def register_user(email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False
    
    new_user = User(email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        print(f'Error registering user: {e}')
        return False
     
def user_login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return True
    else:
        return False
    
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = register_user(email, password)
        if user:
            login_user(user)
            flash('Registration successful!')
            return redirect(url_for('dashboard'))
        else:
            return render_template('register.html', form = form, error = 'Failed to register, please check your email or password.')
    return render_template('register.html', form=form)
    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        success = user_login_user(email, password)
        if success:
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form = form, error='Failed to login, please check your email or password')
    return render_template('login.html', form=form)
