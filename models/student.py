# models/student.py
from database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(15), nullable=False)  # Phone number (same as username)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    bed_no = db.Column(db.Integer)

    def __repr__(self):
        return f'<Student {self.name}>'