from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # Asegúrate de importar UserMixin
from .extensions import db

class User(db.Model, UserMixin):  # Hereda de UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    profile_picture = db.Column(db.String(256), nullable=True)  # Campo para la URL de la foto

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
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    user = db.relationship('User', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')