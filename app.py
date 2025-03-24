from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, init_db
from models.user import User
from models.student import Student
from models.room import Room
from models.complaint import Complaint

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
init_db(app)

# Initialize default users (run once or remove after initial setup)
with app.app_context():
    if not User.query.filter_by(username='1234567890').first():  # Sample admin phone
        admin = User(username='1234567890', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()
    
    if not User.query.filter_by(username='9876543210').first():  # Sample student phone
        student_user = User(username='9876543210', password=generate_password_hash('student123'), role='student')
        db.session.add(student_user)
        student = Student(name='John Doe', roll_no='student1', contact='9876543210')
        db.session.add(student)
        db.session.commit()

# General Login Route (for students)
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.role == 'admin':
            return redirect(url_for('admin_login'))
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        phone_number = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=phone_number).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        flash('Invalid phone number or password', 'error')
    return render_template('login.html')

# Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'user_id' in session and User.query.get(session['user_id']).role == 'admin':
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        phone_number = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=phone_number, role='admin').first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin phone number or password', 'error')
    return render_template('admin/login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    students = Student.query.all()  # Fetch all students, including registered ones
    rooms = Room.query.all()
    complaints = Complaint.query.all()
    return render_template('admin/dashboard.html', students=students, rooms=rooms, complaints=complaints)

# Add Student
@app.route('/admin/add_student', methods=['GET', 'POST'])
def add_student():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        phone_number = request.form['phone_number']
        student = Student(name=name, roll_no=roll_no, contact=phone_number)  # Ensure contact matches phone_number
        db.session.add(student)
        db.session.commit()
        if not User.query.filter_by(username=phone_number).first():
            student_user = User(username=phone_number, password=generate_password_hash(phone_number), role='student')
            db.session.add(student_user)
            db.session.commit()
        flash('Student added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_student.html')

# Add Room
@app.route('/admin/add_room', methods=['GET', 'POST'])
def add_room():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        room_no = request.form['room_no']
        capacity = request.form['capacity']
        room = Room(room_no=room_no, capacity=capacity)
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_room.html')

# Assign Room/Bed
@app.route('/admin/assign_room/<int:student_id>', methods=['GET', 'POST'])
def assign_room(student_id):
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        room_id = request.form['room_id']
        bed_no = request.form['bed_no']
        room = Room.query.get(room_id)
        if len(room.students) < room.capacity:
            student.room_id = room_id
            student.bed_no = bed_no
            db.session.commit()
            flash('Room and bed assigned successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Room capacity full!', 'error')
    rooms = Room.query.all()
    return render_template('admin/assign_room.html', student=student, rooms=rooms)

# Reply to Complaint
@app.route('/admin/reply_complaint/<int:complaint_id>', methods=['GET', 'POST'])
def reply_complaint(complaint_id):
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    complaint = Complaint.query.get_or_404(complaint_id)
    if request.method == 'POST':
        reply = request.form['reply']
        complaint.reply = reply
        complaint.status = 'Resolved'
        db.session.commit()
        flash('Complaint replied successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/reply_complaint.html', complaint=complaint)

# User Dashboard
@app.route('/user/dashboard')
def user_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(contact=user.username).first()  # Use contact (phone number) instead of roll_no
    if not student:
        flash('Student details not found. Please contact admin.', 'error')
        return redirect(url_for('login'))
    return render_template('user/dashboard.html', student=student)

# Register Complaint
@app.route('/user/register_complaint', methods=['GET', 'POST'])
def register_complaint():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    print(f"User username: {user.username}")  # Debug print
    student = Student.query.filter_by(contact=user.username).first()
    print(f"Student found: {student}")  # Debug print
    if not student:
        flash('Student not found. Please contact admin or ensure your profile is registered.', 'danger')
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        description = request.form['description']
        complaint = Complaint(student_id=student.id, description=description)
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint registered successfully', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('user/register_complaint.html')

# Admin Route to Create Users
@app.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(username=phone_number).first():
            flash('Phone number already exists', 'error')
            return redirect(url_for('create_user'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=phone_number, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        if role == 'student':
            student = Student(name=request.form.get('name', phone_number), roll_no=request.form.get('roll_no', ''), contact=phone_number)
            db.session.add(student)
            db.session.commit()
        flash(f'User with phone number {phone_number} created successfully as {role}', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/create_user.html')

# User Registration Route (for students)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        password = request.form['password']
        name = request.form['name']
        roll_no = request.form['roll_no']
        if User.query.filter_by(username=phone_number).first():
            flash('Phone number already registered', 'error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=phone_number, password=hashed_password, role='student')
        db.session.add(new_user)
        db.session.commit()
        student = Student(name=name, roll_no=roll_no, contact=phone_number)  # Ensure contact matches username
        db.session.add(student)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin/delete_student/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    student = Student.query.get_or_404(student_id)
    # Delete associated complaints first
    Complaint.query.filter_by(student_id=student_id).delete()
    # Delete the student
    db.session.delete(student)
    # Check and delete associated user if exists
    user = User.query.filter_by(username=student.contact).first()
    if user:
        db.session.delete(user)
    db.session.commit()
    flash(f'Student {student.name} deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)