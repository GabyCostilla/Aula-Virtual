from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm, CourseForm
from .models import User, Course
from .extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Lógica para manejar el inicio de sesión
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # Verifica si el formulario fue enviado y es válido
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data  # Asegúrate de hashear la contraseña aquí
        )
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))  # Redirigir a la página de inicio de sesión
    return render_template('register.html', form=form)  # Mostrar el formulario si es GET o hay errores

@main_bp.route('/courses', methods=['GET'])
def list_courses():
    courses = Course.query.all()  # Obtener todos los cursos
    return render_template('courses.html', courses=courses)

@main_bp.route('/create-course', methods=['GET', 'POST'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Curso creado exitosamente.', 'success')
        return redirect(url_for('main.list_courses'))
    return render_template('create_course.html', form=form)