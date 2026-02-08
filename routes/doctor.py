from flask import Blueprint, render_template
from flask_login import login_required, current_user

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@doctor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'doctor':
        return "Access Denied", 403

    return render_template('doctor/dashboard.html')
