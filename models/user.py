# models/user.py
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Phone number
    password = db.Column(db.String(100), nullable=False)  # Hashed password
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'student'

    def __repr__(self):
        return f'<User {self.username}>'