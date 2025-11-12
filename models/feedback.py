from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint
from extensions import db


class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id: int = db.Column(db.Integer, primary_key=True)

    schedule_id: int = db.Column(
        db.Integer,
        db.ForeignKey("class_schedules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    teacher_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    student_id: Optional[int] = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    rating: Optional[int] = db.Column(db.SmallInteger, nullable=True)

    comment: Optional[str] = db.Column(db.Text, nullable=True)

    visibility: str = db.Column(
        db.String(32),
        nullable=False,
        default="private", 
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    schedule = db.relationship(
        "ClassSchedule",
        back_populates="feedbacks",
        passive_deletes=True,
    )

    student = db.relationship(
        "Student",
        backref=db.backref("feedbacks", lazy="dynamic"),
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            "(rating IS NULL) OR (rating BETWEEN 1 AND 5)",
            name="ck_feedback_rating_range",
        ),
        db.Index("idx_feedback_teacher_created", "teacher_id", "created_at"),
        db.Index("idx_feedback_student_created", "student_id", "created_at"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Feedback id={self.id} schedule_id={self.schedule_id} teacher_id={self.teacher_id}>"