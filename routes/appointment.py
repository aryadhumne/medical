from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.appointment import Appointment

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointment')

@appointment_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if current_user.role != 'patient':
        flash("Access denied")
        return redirect(url_for('home'))

    if request.method == 'POST':
        appointment = Appointment(
            patient_id=current_user.id,
            department=request.form['department'],
            date=request.form['date'],
            time=request.form['time'],
            reason=request.form.get('reason'),
            status="Pending"
        )

        db.session.add(appointment)
        db.session.commit()

        flash("Appointment request sent successfully")
        return redirect(url_for('patient.dashboard'))

    return render_template('appointment/book.html')
