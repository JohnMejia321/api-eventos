from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@localhost/nombredelabasededatos'  # Reemplaza con tus propios datos
db = SQLAlchemy(app)
