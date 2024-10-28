from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from .forms import RegistrationForm, LoginForm, CourseForm, ProfileUpdateForm, TaskForm, SubmissionForm
from .models import User, Course, Enrollment, Task, Submission
from .extensions import db
from flask_login import current_user, login_required, login_user, logout_user
import os
from werkzeug.utils import secure_filename
import secrets

main_bp = Blueprint('main', __name__)

# Index route
@main_bp.route('/')
def index():
    return render_template('index.html')

# Login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('main.index'))
        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

# Register route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# List all courses
@main_bp.route('/courses')
@login_required
def list_courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

# Create a new course
@main_bp.route('/create-course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            creator_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        flash('Curso creado exitosamente.', 'success')
        return redirect(url_for('main.list_courses'))
    return render_template('create_course.html', form=form)

# Course details
@main_bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

# Enroll in a course
@main_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if enrollment:
        flash('Ya estás inscrito en este curso.', 'warning')
    else:
        db.session.add(Enrollment(user_id=current_user.id, course_id=course_id))
        db.session.commit()
        flash('¡Te has inscrito correctamente en el curso!', 'success')
    return redirect(url_for('main.list_courses'))

# Delete a course
@main_bp.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.creator_id:
        flash('No tienes permiso para eliminar este curso.', 'danger')
    else:
        db.session.delete(course)
        db.session.commit()
        flash('El curso ha sido eliminado correctamente.', 'success')
    return redirect(url_for('main.list_courses'))

# Create a new task for a course
@main_bp.route('/course/<int:course_id>/create-task', methods=['GET', 'POST'])
@login_required
def create_task(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.creator_id:
        flash('No tienes permiso para agregar tareas a este curso.', 'danger')
        return redirect(url_for('main.course_detail', course_id=course_id))

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            course_id=course.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Tarea creada exitosamente.', 'success')
        return redirect(url_for('main.course_detail', course_id=course.id))
    return render_template('create_task.html', form=form, course=course)

# Profile route
@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()
    user_courses = Enrollment.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        db.session.commit()
        flash('Tu perfil ha sido actualizado.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile.html', user=current_user, courses=user_courses, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

# Logout route
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('main.index'))

# Submission helper function
def save_submission_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    filepath = os.path.join(current_app.root_path, 'static/submissions', filename)
    file.save(filepath)
    return filename

# Submit a task
@main_bp.route('/task/<int:task_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = SubmissionForm()
    if form.validate_on_submit() and form.file.data:
        filename = save_submission_file(form.file.data)
        submission = Submission(file_path=filename, task_id=task_id, student_id=current_user.id)
        db.session.add(submission)
        db.session.commit()
        flash('Tarea entregada con éxito.', 'success')
        return redirect(url_for('main.task_detail', task_id=task_id))
    return render_template('submit_task.html', task=task, form=form)

# Task details
@main_bp.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    submissions = Submission.query.filter_by(task_id=task_id).all()
    return render_template('task_detail.html', task=task, submissions=submissions)
