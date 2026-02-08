from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager
from flask_login import login_required, current_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Tell Flask-Login where login page is
    login_manager.login_view = 'auth.login'

    # ---- REGISTER BLUEPRINTS ----
    from routes.auth import auth_bp
    from routes.patient import patient_bp
    from routes.doctor import doctor_bp
    from routes.appointment import appointment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(appointment_bp)

    # ---- ROOT ROUTE ----
    @app.route('/')
    def home():
        # Always open login page first
        return redirect(url_for('auth.login'))

    # ---- COMMON DASHBOARD ROUTE ----
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'patient':
            return redirect(url_for('patient.dashboard'))

        elif current_user.role == 'doctor':
            return redirect(url_for('doctor.dashboard'))

        else:
            return "Invalid role"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
