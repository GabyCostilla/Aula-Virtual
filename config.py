import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario_aula:password_seguro@localhost/aula_virtual_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True