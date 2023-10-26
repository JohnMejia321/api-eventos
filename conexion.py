from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError  # Importa la excepción OperationalError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fredy555@localhost/eventos'
db = SQLAlchemy(app)
# Vincula la aplicación con SQLAlchemy

try:
    with app.app_context():
        db.create_all()
except OperationalError as e:
    print(f"Error al crear la base de datos: {e}")

