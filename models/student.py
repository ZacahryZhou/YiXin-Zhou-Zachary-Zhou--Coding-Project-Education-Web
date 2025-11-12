from extensions import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'  

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(25), nullable=True)
    course = db.Column(db.String(64), nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tuition_records = db.relationship(
        'Tuition',
        backref='student',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'


class Tuition(db.Model):
    __tablename__ = 'tuition'  
    id = db.Column(db.Integer, primary_key=True)

    
    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id', ondelete='CASCADE'),
        nullable=False
    )

    mode = db.Column(db.String(20), nullable=False, default='lesson')
    tuition_amount = db.Column(db.Float, nullable=False)
    rate_per_lesson = db.Column(db.Float, nullable=False, default=0.0)
    rate_per_hour = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, nullable=False, default=0.0)
    lesson_quantity = db.Column(db.Float)
    duration_hours = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(100))

    def __repr__(self):
        return f'<Tuition: {self.tuition_amount} for student {self.student_id}>'