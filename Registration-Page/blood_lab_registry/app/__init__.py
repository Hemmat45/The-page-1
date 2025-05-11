
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_lab.db'
app.secret_key = 'dev-secret-key'

db = SQLAlchemy(app)

from app import routes, models

with app.app_context():
    db.create_all()
