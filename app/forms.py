from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField, PasswordField, FileField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CourseForm(FlaskForm):
    name = StringField('Nombre del Curso', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    start_date = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de Finalización', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Crear Curso')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    due_date = DateField('Fecha de entrega', validators=[DataRequired()])
    submit = SubmitField('Añadir Tarea')

class ProfileUpdateForm(FlaskForm):
    picture = FileField('Actualizar Foto de Perfil', validators=[DataRequired()])
    submit = SubmitField('Actualizar Foto')  

class SubmissionForm(FlaskForm):
    file = FileField('Subir Tarea', validators=[DataRequired()])
    submit = SubmitField('Enviar')