from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:fredy555@localhost/eventos'
db = SQLAlchemy(app)
# Vincula la aplicación con SQLAlchemy

