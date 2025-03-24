# LLAI Hostel Management System

## Introduction
The **LLAI Hostel Management System** is a web-based application designed to efficiently manage hostel operations, including student registrations, room allocations, complaints, and user authentication. Built using **Flask**, this system leverages an SQLite database to store hostel-related information.

## Description
This project provides an automated solution for hostel management, reducing manual efforts in handling student details, room allocations, and complaint resolutions. It ensures a seamless experience for both administrators and students through a user-friendly web interface.

## Features
- User Authentication (Admin & Students)
- Student Registration & Management
- Room Allocation & Tracking
- Complaint Management System
- Database Integration (SQLite)
- Web-based User Interface

## Technologies Used
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Other:** Jinja Templating, Flask-WTF (Forms)

## Installation & Setup
### Prerequisites
Ensure you have Python installed on your system (Python 3.7 or later).

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd LLAI-Hostel-Management-System
```

### Step 2: Create & Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize the Database
```bash
python database.py
```

### Step 5: Run the Application
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000/`

## Project Structure
```
LLAI Hostel Management System/
│── app.py                  # Main application file
│── database.py              # Database setup script
│── requirements.txt         # Project dependencies
│── instance/
│   └── hostel.db            # SQLite database
│── models/                  # Database models
│   ├── complaint.py
│   ├── room.py
│   ├── student.py
│   ├── user.py
│── templates/               # HTML templates (Frontend)
│── static/                  # CSS, JS, images
└── README.md                # Project documentation
```

## Usage
- **Admin Dashboard:** Manage students, rooms, and complaints.
- **Student Portal:** Submit complaints, check room details.

## Contribution
Feel free to fork this repository and submit pull requests for improvements.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please reach out to the project owner.

---
Developed by **Vishnu**

