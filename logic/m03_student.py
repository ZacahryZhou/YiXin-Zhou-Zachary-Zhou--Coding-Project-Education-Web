from flask import Blueprint, render_template, redirect, url_for, flash
from forms.m03_student import StudentForm, TuitionForm
from flask_login import login_required, current_user
from models.student import Student, Tuition
from extensions import db
from datetime import datetime

student_bp = Blueprint('student', __name__)


def calculate_tuition_amount(mode, lesson_quantity, duration_hours, rate_per_lesson, rate_per_hour):
    if mode == 'lesson':
        return round((lesson_quantity or 0.0) * (rate_per_lesson or 0.0), 2)
    elif mode == 'duration_hours':
        return round((duration_hours or 0.0) * (rate_per_hour or 0.0), 2)
    return 0.0


@student_bp.route('/student', methods=['GET', 'POST'])
@login_required
def student():
    s_form = StudentForm()
    if s_form.validate_on_submit():
        new_student = Student(
            first_name=s_form.first_name.data,
            last_name=s_form.last_name.data,
            age=s_form.age.data,
            grade=s_form.grade.data,
            email=s_form.email.data,
            phone=s_form.phone.data,
            course=s_form.course.data,
            teacher_id=current_user.id
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully', 'success')
        return redirect(url_for('student.student'))
    elif s_form.errors:
        flash('Please fill in all required fields correctly', 'danger')

    return render_template('m03_student.html', s_form=s_form, students=get_all_students())


@student_bp.route('/student/<int:student_id>/tuition', methods=['GET', 'POST'])
@login_required
def tuition(student_id):
    student = Student.query.get_or_404(student_id)
    t_form = TuitionForm()
    tuition_records = Tuition.query.filter_by(student_id=student.id).all()

    
    tuition_amount = calculate_tuition_amount(
        t_form.mode.data,
        t_form.lesson_quantity.data,
        t_form.duration_hours.data,
        t_form.rate_per_lesson.data,
        t_form.rate_per_hour.data
    )

    total_tuition_amount = sum(t.tuition_amount or 0.0 for t in tuition_records)
    total_lessons = sum(t.lesson_quantity or 0.0 for t in tuition_records)
    total_paid_amount = sum(t.paid_amount or 0.0 for t in tuition_records)
    balance = round(total_tuition_amount - total_paid_amount, 2)

    return render_template(
        'm03_student_tuition.html',
        student=student,
        tuition_records=tuition_records,
        t_form=t_form,
        total_lessons=total_lessons,
        total_paid_amount=total_paid_amount,
        balance=balance,
        total_tuition_amount=total_tuition_amount
    )


@student_bp.route('/student/<int:student_id>/add_tuition', methods=['POST'])
@login_required
def add_tuition(student_id):
    student = Student.query.get_or_404(student_id)
    t_form = TuitionForm()

    if t_form.validate_on_submit():
        mode = t_form.mode.data
        tuition_amount = calculate_tuition_amount(
            mode,
            t_form.lesson_quantity.data,
            t_form.duration_hours.data,
            t_form.rate_per_lesson.data,
            t_form.rate_per_hour.data
        )

        new_tuition = Tuition(
            student_id=student.id,
            lesson_quantity=t_form.lesson_quantity.data if mode == 'lesson' else None,
            duration_hours=t_form.duration_hours.data if mode == 'duration_hours' else None,
            rate_per_lesson=t_form.rate_per_lesson.data,
            rate_per_hour=t_form.rate_per_hour.data,
            paid_amount=t_form.paid_amount.data,
            note=t_form.note.data,
            mode=mode,
            tuition_amount=tuition_amount,
            timestamp=datetime.utcnow()
        )

        try:
            db.session.add(new_tuition)
            db.session.commit()
            flash("Tuition record added successfully.", "success")
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Failed to add tuition: {e}")
            flash("Failed to add tuition record.", "danger")
    else:
        print("[DEBUG] Form validation failed.")
        for field, errors in t_form.errors.items():
            print(f"[DEBUG] Validation error in '{field}': {errors}")
        flash("Invalid form data. Please check required fields.", "danger")

    return redirect(url_for('student.tuition', student_id=student.id))


@student_bp.route('/student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash(f'Student information updated successfully for {student.first_name} {student.last_name}', 'success')
        return redirect(url_for('student.student_detail', student_id=student.id))

    return render_template('m03_student_detail.html', student=student, form=form)


@student_bp.route('/student/<int:student_id>/delete_student', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash(f'{student.first_name} {student.last_name} has been deleted', 'success')
    return redirect(url_for('student.student'))


def get_all_students():
    return Student.query.all()