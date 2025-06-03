# Student Management System

A comprehensive web application for managing student records, subjects, and grades.

## Features
- Student profile management
- Subject enrollment tracking
- Grade management (activities, quizzes, exams)
- RESTful API for data operations
- User-friendly web interface

## Technologies Used
- Backend: Django with Django REST Framework
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (development) / PostgreSQL (production)
- API: RESTful architecture

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps
1. Clone the repository
```bash
git clone <repository-url>
cd student-management-system
```

2. Set up a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run database migrations
```bash
python manage.py migrate
```

5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

6. Start the development server
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Project Structure
- `backend/` - Django backend code
- `frontend/` - HTML/CSS/JS frontend code
- `docs/` - Project documentation and screenshots

## API Endpoints
- `/api/students/` - Student CRUD operations
- `/api/subjects/` - Subject CRUD operations
- `/api/grades/` - Grade CRUD operations

## Contributors
- John Michael Cadorna
- Harvey Verian
