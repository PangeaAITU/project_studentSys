# 🎓 Student Management System

A Django-based Student Management System for managing students, teachers, classes, subjects, and grades.

## ✨ Features

- 👥 User Management with role-based access (Admin, Teacher, Student)
- 🏫 Classroom Management
- 📚 Subject Management
- 📝 Grade Tracking
- 🔐 Secure Authentication
- 📊 Student Performance Analytics
- 📱 REST API

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd project_studentSys
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create logs directory**
```bash
mkdir logs
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## 📁 Project Structure

```
project_studentSys/
├── sms/              # Project settings
├── users/            # User management
├── school/           # School management
├── grades/           # Grade management
├── templates/        # HTML templates
├── static/           # Static files
├── media/            # User uploads
└── logs/            # Application logs
```

## 👥 User Roles

### Administrator
- Full system access
- Manage all users and settings

### Teacher
- Manage assigned classes
- Add/edit student grades
- View student information

### Student
- View own grades and profile
- View class information

## 🔧 Configuration

Create a `.env` file in the project root (optional):
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📝 Usage

### Add a Student
1. Go to Admin Panel
2. Click "Users" → "Add User"
3. Create user account
4. Edit Profile → Set role to "Student"

### Add a Grade
1. Go to Admin Panel
2. Click "Grades" → "Add Grade"
3. Select student, subject, and enter value

## 🧪 Testing

```bash
python manage.py test
```

## 📄 License

MIT License

## 👨‍💻 Development Team

CS-2409 Group