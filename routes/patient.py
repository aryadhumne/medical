import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models.patient import Patient
from extensions import db

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

# ================= DASHBOARD =================

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        flash("Access denied")
        return redirect(url_for('home'))

    patient = Patient.query.filter_by(user_id=current_user.id).first()
    return render_template('patient/dashboard.html', patient=patient)


# ================= MEDICAL PROFILE =================

@patient_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'patient':
        flash("Access denied")
        return redirect(url_for('home'))

    patient = Patient.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        if not patient:
            patient = Patient(user_id=current_user.id)

        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.blood_group = request.form['blood_group']
        patient.allergies = request.form['allergies']
        patient.chronic_diseases = request.form['chronic_diseases']
        patient.emergency_contact = request.form['emergency_contact']

        db.session.add(patient)
        db.session.commit()

        flash("Medical profile updated", "success")
        return redirect(url_for('patient.dashboard'))

    return render_template('patient/profile.html', patient=patient)


# ================= MEDICAL RECORD UPLOAD (FIXED) =================

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@patient_bp.route('/upload-record', methods=['GET', 'POST'])
@login_required
def upload_record():
    if current_user.role != 'patient':
        flash("Access denied")
        return redirect(url_for('home'))

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if request.method == 'POST':
        file = request.files.get('record')

        if not file or file.filename == "":
            flash("No file selected", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file type", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        flash("Medical record uploaded successfully!", "success")
        return redirect(url_for('patient.upload_record'))

    # 📂 LIST ALL UPLOADED FILES
    records = os.listdir(UPLOAD_FOLDER)

    return render_template(
        'patient/upload_record.html',
        records=records
    )
# ================= EMERGENCY =================

@patient_bp.route('/emergency')
@login_required
def emergency():
    if current_user.role != 'patient':
        flash("Access denied")
        return redirect(url_for('home'))

    patient = Patient.query.filter_by(user_id=current_user.id).first()
    return render_template('patient/emergency.html', patient=patient)
