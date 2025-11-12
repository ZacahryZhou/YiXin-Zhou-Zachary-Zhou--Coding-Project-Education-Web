from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FloatField, IntegerField, URLField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class CourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired(), Length(max=64)])
    course_description = TextAreaField('Course Description', validators=[Optional(), Length(max=256)])
    subject = StringField('Subject', validators=[Optional(), Length(max=64)])
    course_duration = FloatField('Course Duration (hours)', validators=[Optional(), NumberRange(min=0.01, message='Must be > 0')])
    teacher = StringField('Teacher', validators=[Optional(), Length(max=64)])
    submit = SubmitField('Submit')

class CourseSectionForm(FlaskForm):
    title = StringField('Section Title', validators=[DataRequired(), Length(max=64)])
    content = TextAreaField('Section Content', validators=[DataRequired()])
    description = TextAreaField('Section Description', validators=[Optional(), Length(max=500)])
    section_order = IntegerField('Section Order', validators=[Optional(), NumberRange(min=1, message='Must be >= 1')])
    section_URL = URLField('URL', validators=[Optional(), Length(max=512)])
    submit_section = SubmitField('Submit')