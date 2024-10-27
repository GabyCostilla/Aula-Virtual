from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):  # Hereda de UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    profile_picture = db.Column(db.String(256), nullable=True)  # Campo para la URL de la foto
    courses_created = db.relationship('Course', backref='creator', lazy=True)

    def set_password(self, password):
        """Establece la contraseña hasheada para el usuario."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la contraseña hasheada."""
        return check_password_hash(self.password, password)

    # Métodos requeridos por Flask-Login
    @property
    def is_active(self):
        return True  # O implementa tu lógica si necesitas

    @property
    def is_authenticated(self):
        return True  # Esto es verdadero para todos los usuarios autenticados

    @property
    def is_anonymous(self):
        return False  # Nunca debería ser anónimo si está autenticado

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    tasks = db.relationship('Task', back_populates='course', cascade='all, delete-orphan')


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    user = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # Foreign key to course.id

    course = db.relationship('Course', back_populates='tasks')


