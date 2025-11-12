from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, TextAreaField, SubmitField, FloatField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Optional

class StudentForm(FlaskForm):
    first_name = StringField('first Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('last Name', validators=[Optional(), Length(max=50)])
    email = StringField('email', validators=[Optional(), Email(), Length(max=200)])
    grade = StringField('grade', validators=[Optional(), Length(max=20)])
    age = IntegerField('age', validators=[Optional()])
    gender = SelectField('gender', choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ], validators=[DataRequired()])
    phone = StringField('phone',validators=[Optional(), Length(max=30)])
    course = StringField('Course', validators=[Optional(), Length(max=64)])
    submit = SubmitField('submit')


def round_time(form, field):
    value  = field.data
    if value is not None:
        try:
            rounded = round(value, 1)
            if value != rounded:
                raise ValidationError(f'Please enter a valid number with one decimal place, got {value}')
        except ValueError:
            raise ValidationError(f'Please enter a valid number, got {value}')
        



class TuitionForm(FlaskForm):
    mode = SelectField('mode', 
                       choices=[

                           ('lesson', 'Lesson'), 
                           ('duration_hours', 'Duration')
                       ],
                       validators=[DataRequired()],
                       coerce=str
                      )
    
    tuition_amount = FloatField('amount', validators=[Optional()])
    rate_per_lesson = FloatField('Rate per Lesson', validators=[Optional(), round_time], default=0.0)
    rate_per_hour = FloatField('Rate per Hour', validators=[Optional(), round_time], default=0.0)
    paid_amount = FloatField('Paid Amount', validators=[Optional(), round_time], default=0.0)
    lesson_quantity = FloatField('Number of Lessons', validators=[Optional(), round_time])
    duration_hours = FloatField('Duration in Hours', validators=[Optional(), round_time])
    note = TextAreaField('note', validators=[Optional(), Length(max=500)])
    submit = SubmitField('submit')


