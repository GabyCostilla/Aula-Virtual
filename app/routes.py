from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import RegistrationForm, LoginForm, CourseForm
from .models import User, Course, Enrollment  # Asegúrate de importar Enrollment
from .extensions import db
from flask_login import current_user, login_required, login_user # Importar current_user y login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash('No se encontró el usuario.', 'danger')
                return render_template('login.html', form=form)

            print(f"Usuario encontrado: {user.username}, Contraseña: {user.password}")  # Para depuración

            if user.check_password(form.password.data):
                login_user(user)
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Correo o contraseña incorrectos.', 'danger')
        except Exception as e:
            flash('Ocurrió un error al iniciar sesión. Por favor, intenta de nuevo.', 'danger')
            print(f"Error: {e}")  # Imprimir el error en la consola
    return render_template('login.html', form=form)



@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)  # Asegúrate de hashear la contraseña aquí
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_bp.route('/courses', methods=['GET'])
@login_required  # Solo los usuarios logueados pueden acceder a los cursos
def list_courses():
    # Depuración: Imprimir si el usuario está autenticado
    print(f"Usuario autenticado: {current_user.is_authenticated}")  # Esto debería imprimir True si el usuario ha iniciado sesión correctamente
    
    # Obtener todos los cursos
    courses = Course.query.all()  
    
    # Renderizar la plantilla con la lista de cursos
    return render_template('courses.html', courses=courses)

@main_bp.route('/create-course', methods=['GET', 'POST'])
@login_required  # Solo los usuarios logueados pueden crear cursos
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

@main_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required  # Solo los usuarios logueados pueden inscribirse en un curso
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Verificar si el usuario ya está inscrito en el curso
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    
    if enrollment:
        flash('Ya estás inscrito en este curso.', 'warning')
    else:
        # Crear la inscripción
        new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()
        flash('¡Te has inscrito correctamente en el curso!', 'success')
    
    return redirect(url_for('main.list_courses'))
