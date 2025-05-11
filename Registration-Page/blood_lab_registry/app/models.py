
from app import db
from datetime import datetime

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    whatsapp_no = db.Column(db.String(20))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_code = db.Column(db.String(20), unique=True, nullable=False)
    registration_date_time = db.Column(db.DateTime, default=datetime.utcnow)
    courtesy_title = db.Column(db.String(20))
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    age_unit = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    whatsapp_no = db.Column(db.String(20))
    referred_by = db.Column(db.String(100))

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    total_amount = db.Column(db.Float)
    discount = db.Column(db.Float, default=0)
    paid_amount = db.Column(db.Float)
    balance = db.Column(db.Float)
    selected_tests = db.Column(db.Text)  # Store as JSON string
