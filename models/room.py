# models/room.py
from database import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    students = db.relationship('Student', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.room_no}>'