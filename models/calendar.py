from datetime import datetime
from extensions import db
from sqlalchemy import CheckConstraint

class ClassSchedule(db.Model):
    __tablename__ = 'class_schedules'

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    section_id = db.Column(
        db.Integer,
        db.ForeignKey('course_sections.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))

    start_time = db.Column(db.DateTime, nullable=False)  
    end_time   = db.Column(db.DateTime, nullable=True)   
    all_day    = db.Column(db.Boolean, default=False)

    location = db.Column(db.String(256))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    student = db.relationship(
        "Student",
        backref=db.backref("schedules", lazy="dynamic"),
        passive_deletes=True
    )

    course = db.relationship(
        "Course",
        backref=db.backref("schedules", lazy="dynamic"),
        passive_deletes=True
    )

    section = db.relationship(
        "CourseSection",
        back_populates="schedules",
        passive_deletes=True
    )

    
    feedbacks = db.relationship(
    "Feedback",
    back_populates="schedule",
    cascade="all, delete-orphan",
    passive_deletes=True
   )

    __table_args__ = (
        db.Index("idx_clsched_teacher_start_time", "teacher_id", "start_time"),
        db.Index("idx_clsched_teacher_student", "teacher_id", "student_id"),
        db.Index("idx_clsched_teacher_course",  "teacher_id", "course_id"),
        db.Index("idx_clsched_teacher_section", "teacher_id", "section_id"),
        CheckConstraint("(end_time IS NULL) OR (end_time >= start_time)", name="ck_end_ge_start"),
    )