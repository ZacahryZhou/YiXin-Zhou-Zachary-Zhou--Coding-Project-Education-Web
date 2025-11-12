from flask import Flask, render_template, flash, Blueprint, redirect, url_for
from forms.m02_user import UserForm
from models.user import User
from extensions import db
from flask_login import current_user, login_required

profile_bp = Blueprint('profile', __name__)
@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserForm()
    

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.gender = form.gender.data
        current_user.phone = form.phone.data
        current_user.links = form.links.data

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile'))
    elif form.errors:
        flash('First Name and Last Name and Email; gender are required', 'error')

    if not form.is_submitted():
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.gender.data = current_user.gender
        form.phone.data = current_user.phone
        form.links.data = current_user.links
    return render_template('m02_user.html', form=form)
