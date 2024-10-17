from flask import Flask
from flask_migrate import Migrate
from .extensions import db, login_manager  # Asegúrate de que db y login_manager están importados desde extensions.py
from .models import User  # Importar el modelo User

def create_app():
    app = Flask(__name__)

    # Cargar la configuración desde config.py
    app.config.from_object('config.Config')

    # Inicializar las extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)  # Integración de Flask-Migrate para migraciones de base de datos

    # Registrar Blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Cargar el usuario desde la sesión cuando el login_manager lo necesite
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Devuelve el usuario por ID desde la base de datos

    return app
