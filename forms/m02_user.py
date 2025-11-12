from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    first_name = StringField('first Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(max=200)])
    gender = SelectField('gender', choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ], validators=[DataRequired()])

    phone = StringField('phone')
    links = StringField('links')
    submit = SubmitField('submit')