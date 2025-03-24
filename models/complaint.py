from database import db
from models.student import Student

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    reply = db.Column(db.String(500))
    status = db.Column(db.String(50), default='Pending')

    student = db.relationship('Student', backref='complaints')