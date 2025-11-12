from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from forms.m04_course import CourseForm, CourseSectionForm
from models.course import Course, CourseSection
from extensions import db


course_bp = Blueprint('course', __name__, url_prefix='/courses')


def get_all_courses():
    return (Course.query
            .filter_by(teacher_id=current_user.id)
            .order_by(Course.created_at.desc())
            .all())



@course_bp.route('/course', methods=['GET', 'POST'])
@login_required
def course():
    c_form = CourseForm()
    if c_form.validate_on_submit():
        new_course = Course(
            teacher_id=current_user.id,
            course_name=c_form.course_name.data,
            course_description=c_form.course_description.data or None,
            subject=c_form.subject.data or None,
            teacher=c_form.teacher.data,
            course_duration=c_form.course_duration.data
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Course added successfully', 'success')
        return redirect(url_for('course.course'))
    elif c_form.errors:
        flash('Please fill in all required fields correctly', 'danger')

    return render_template(
        'm04_course.html',
        c_form=c_form,
        courses=get_all_courses()
    )



@course_bp.route('/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        abort(403)

    
    name = course.course_name
    subject = course.subject or ''

    db.session.delete(course)
    db.session.commit()
    flash(f'{name} {subject} has been deleted', 'success')
    return redirect(url_for('course.course'))



@course_bp.route('/<int:course_id>/sections', methods=['GET', 'POST'])
@login_required
def course_sections(course_id):
    course = Course.query.get_or_404(course_id)
    if course.teacher_id != current_user.id:
        abort(403)

    c_s_form = CourseSectionForm()
    c_form = CourseForm()  

    
    try:
        sections_query = course.sections
        course_sections = sections_query.order_by(CourseSection.section_order.asc()).all()
    except AttributeError:
        
        course_sections = sorted(course.sections, key=lambda s: (s.section_order or 0))

    if c_s_form.validate_on_submit():
        order_input = c_s_form.section_order.data
        if order_input is None:
            max_order = (
                db.session.query(func.coalesce(func.max(CourseSection.section_order), 0))
                .filter(CourseSection.course_id == course.id)
                .scalar()
            )
            section_order = int(max_order) + 1
        else:
            section_order = int(order_input)
            
        
        new_course_section = CourseSection(
            course_id=course.id,
            title=c_s_form.title.data,
            content=c_s_form.content.data or None,
            description=c_s_form.description.data or None,
            section_order=section_order
        )
        db.session.add(new_course_section)
        try:
            db.session.commit()
            flash('New Course Section Added Successfully', 'success')
            return redirect(url_for('course.course_sections', course_id=course.id))
        except IntegrityError as e:
            db.session.rollback()
            print("IntegrityError:", getattr(e.orig, "args", e))
            flash(f'Order {section_order} already exists in this course.', 'warning')
        except Exception:
            db.session.rollback()
            flash('Failed to add Course Section', 'danger')
    elif c_s_form.errors:
        flash('Please fill in all required fields correctly', 'danger')

    return render_template(
        'm04_course_section.html',
        c_form=c_form,
        c_s_form=c_s_form,
        course_sections=course_sections,
        course=course
    )


@course_bp.route('/sections/<int:section_id>/delete', methods=['POST'])
@login_required
def delete_section(section_id):
    csec = CourseSection.query.get_or_404(section_id)
    if csec.course.teacher_id != current_user.id:
        abort(403)

    title = csec.title
    course_id = csec.course_id

    db.session.delete(csec)
    db.session.commit()

    flash(f'{title} has been deleted', 'success')
    return redirect(url_for('course.course_sections', course_id=course_id))