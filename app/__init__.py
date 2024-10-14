from flask import Flask
from flask_migrate import Migrate
from .extensions import db, login_manager
from .models import User  # Importar el modelo aquí

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
