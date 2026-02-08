from extensions import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    blood_group = db.Column(db.String(10))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    chronic_diseases = db.Column(db.Text)
    emergency_contact = db.Column(db.String(15))

    def __repr__(self):
        return f"<Patient {self.user_id}>"
