import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta')
    
    # Configura la URI de conexión utilizando las variables de entorno de Clever Cloud
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'MYSQL_ADDON_URI',
        'mysql+pymysql://uwxekpvh8fps6jpj:6pXWq9c3e2ptjrVMfmhJ@bl1l7thyu07qhb4xsk7y-mysql.services.clever-cloud.com:3306/bl1l7thyu07qhb4xsk7y'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

# Imprimir la URI para verificar que se asigna correctamente (esto se debe hacer fuera de la clase)
print("DATABASE URI:", Config.SQLALCHEMY_DATABASE_URI)
