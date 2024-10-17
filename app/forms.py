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

class ProfileUpdateForm(FlaskForm):
    picture = FileField('Actualizar Foto de Perfil', validators=[DataRequired()])  # Campo para la carga de la foto
    submit = SubmitField('Actualizar Foto')  # Botón de envío
