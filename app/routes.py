from flask import Blueprint, render_template, redirect, url_for, flash,current_app
from .forms import RegistrationForm, LoginForm, CourseForm, ProfileUpdateForm
from .models import User, Course, Enrollment  # Asegúrate de importar Enrollment
from .extensions import db
from flask_login import current_user, login_required, login_user # Importar current_user y login_required
import os
from werkzeug.utils import secure_filename
import secrets


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

@main_bp.route('/course/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)  # Obtiene el curso por ID
    return render_template('course_detail.html', course=course)  # Muestra la plantilla con el curso


@main_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required  # Asegúrate de que solo los usuarios autenticados puedan inscribirse
def enroll(course_id):
    course = Course.query.get_or_404(course_id)  # Verifica que el curso exista
    
    # Verifica si el usuario ya está inscrito en el curso
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

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()  # Crea una instancia del formulario
    user_courses = Enrollment.query.filter_by(user_id=current_user.id).all()  # Obtener cursos en los que está inscrito el usuario

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # Llama a la función para guardar la imagen
            current_user.profile_picture = picture_file  # Actualiza el campo de foto de perfil en la base de datos
        db.session.commit()  # Guarda cambios en la base de datos
        flash('Tu perfil ha sido actualizado.', 'success')  # Mensaje de éxito
        return redirect(url_for('main.profile'))  # Redirige al perfil del usuario

    return render_template('profile.html', user=current_user, courses=user_courses, form=form)  # Pasa el formulario a la plantilla



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # Genera un nombre de archivo aleatorio
    _, f_ext = os.path.splitext(form_picture.filename)  # Obtiene la extensión del archivo
    picture_fn = random_hex + f_ext  # Combina el nombre aleatorio con la extensión
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # Define la ruta de almacenamiento

    form_picture.save(picture_path)  # Guarda la imagen
    return picture_fn  # Devuelve el nombre del archivo


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # Guarda la imagen
            current_user.profile_picture = picture_file  # Actualiza el campo en el modelo
        db.session.commit()  # Guarda cambios en la base de datos
        flash('Tu perfil ha sido actualizado.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('update_profile.html', form=form)  # Asegúrate de que esta línea esté correcta

