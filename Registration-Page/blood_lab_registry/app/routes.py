
from flask import render_template, request, jsonify
from app import app, db
from app.models import Doctor, Test, Patient, Registration
from datetime import datetime
import json

# Add sample data if not exists
def init_sample_data():
    with app.app_context():
        if not Doctor.query.first():
            doctors = [
                Doctor(name="Dr. Sharma", whatsapp_no="9876543210"),
                Doctor(name="Dr. Patel", whatsapp_no="9876543211"),
                Doctor(name="Dr. Singh", whatsapp_no="9876543212")
            ]
            for doc in doctors:
                db.session.add(doc)
        
        if not Test.query.first():
            tests = [
                Test(code="CBC", name="Complete Blood Count", price=500),
                Test(code="LFT", name="Liver Function Test", price=800),
                Test(code="KFT", name="Kidney Function Test", price=900),
                Test(code="TFT", name="Thyroid Function Test", price=1200),
                Test(code="HBA1C", name="Glycated Hemoglobin", price=600),
                Test(code="LIPID", name="Lipid Profile", price=700),
                Test(code="ESR", name="Erythrocyte Sedimentation Rate", price=300),
                Test(code="CRP", name="C-Reactive Protein", price=450),
                Test(code="URINE", name="Urine Analysis", price=350),
                Test(code="BLOOD", name="Blood Group Test", price=250)
            ]
            for test in tests:
                db.session.add(test)
        
        db.session.commit()

init_sample_data()

@app.route('/')
def home():
    doctors = Doctor.query.all()
    tests = Test.query.all()
    return render_template('registration.html',
        courtesy_titles=["Mr.", "Mrs.", "Ms.", "Smt.", "Shri.", "Master", "Baby-M", "Baby-F"],
        age_units=["Years", "Months", "Weeks", "Days"],
        genders=["Male", "Female", "Other"],
        doctors=doctors,
        tests=tests)

@app.route('/api/patients/next-code')
def get_next_patient_code():
    last_patient = Patient.query.order_by(Patient.id.desc()).first()
    next_code = "1000" if not last_patient else str(int(last_patient.unique_code) + 1)
    return jsonify({"next_code": next_code})

@app.route('/api/doctors/<name>')
def get_doctor(name):
    doctor = Doctor.query.filter_by(name=name).first()
    if doctor:
        return jsonify({"whatsapp_no": doctor.whatsapp_no})
    return jsonify({"error": "Doctor not found"}), 404

@app.route('/api/registrations', methods=['POST'])
def create_registration():
    data = request.json
    try:
        patient = Patient(
            unique_code=data["unique_code"],
            registration_date_time=datetime.fromisoformat(data["registration_date_time"]),
            courtesy_title=data["courtesy_title"],
            name=data["name"],
            age=data["age"],
            age_unit=data["age_unit"],
            gender=data["gender"],
            whatsapp_no=data["whatsapp_no"],
            referred_by=data["referred_by"]
        )
        db.session.add(patient)
        db.session.flush()

        registration = Registration(
            patient_id=patient.id,
            total_amount=data["total_amount"],
            discount=data["discount"],
            paid_amount=data["paid_amount"],
            balance=data["balance"],
            selected_tests=json.dumps(data["selected_tests"])
        )
        db.session.add(registration)
        db.session.commit()

        return jsonify({
            "message": "Registration saved successfully",
            "patient_id": patient.id,
            "registration_id": registration.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
