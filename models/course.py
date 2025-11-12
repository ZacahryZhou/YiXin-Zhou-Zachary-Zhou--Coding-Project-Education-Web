from datetime import datetime
from extensions import db


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    course_name = db.Column(db.String(64), nullable=False)
    course_description = db.Column(db.String(256))
    subject = db.Column(db.String(64))
    teacher = db.Column(db.String(64))
    course_duration = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    sections = db.relationship(
        'CourseSection',
        back_populates='course',
        cascade='all, delete-orphan',
        single_parent=True,
        passive_deletes=True,
        order_by='CourseSection.section_order',
        lazy='selectin'
    )



class CourseSection(db.Model):
    __tablename__ = 'course_sections'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)
    description = db.Column(db.String(500))
    section_order = db.Column(db.Integer)
    section_url = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    course = db.relationship('Course', back_populates='sections')

    schedules = db.relationship(
        'ClassSchedule',
        back_populates='section',
        passive_deletes=True
    )