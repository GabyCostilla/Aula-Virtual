from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    profile_picture = db.Column(db.String(256), nullable=True) 
    courses_created = db.relationship('Course', backref='creator', lazy=True)

    def set_password(self, password):
        """Establece la contraseña hasheada para el usuario."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la contraseña hasheada."""
        return check_password_hash(self.password, password)

    @property
    def is_active(self):
        return True  
    @property
    def is_authenticated(self):
        return True  
    @property
    def is_anonymous(self):
        return False  

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
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  
    course = db.relationship('Course', back_populates='tasks')
    submissions = db.relationship('Submission', backref='task', lazy=True)

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(150), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)  # Relación corregida
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student = db.relationship('User', backref='submissions')  # Relación con User

