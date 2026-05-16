# Software Request Management System

A Django-based web application designed to manage software installation requests submitted by academic and staff users.

The system allows users to:
- Submit software requests
- View previous requests
- Edit active requests
- Renew older requests for a new cycle
- Track request statuses
- Manage request periods through an admin panel

---

# Features

## User Features
- User authentication and login system
- Personal dashboard displaying submitted requests
- Create new software requests
- Edit requests during active request periods
- Renew older requests into the current cycle
- Filter requests by year
- View detailed request information

## Admin Features
- Django admin integration
- Manage software requests
- Manage request cycles
- Change request statuses
- Assign ticket numbers
- Control whether request periods are open or closed

---

# Request Workflow

Each software request progresses through statuses:

- Submitted
- In Review
- Completed

Users can only edit requests when:
- A request cycle is active
- The request belongs to the current year
- The request status is still `Submitted`

---

# Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS

---

# Security Features

- Authentication required for all request pages
- Users can only access their own requests
- Server-side validation for editing and renewal permissions
- Protection against duplicate renewals
- Request cycle restrictions enforced server-side

---

# Project Structure

```text
accounts/
requests/
templates/
static/
manage.py
db.sqlite3
```

---

# Installation

## Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

## Create virtual environment

```bash
python -m venv venv
```

## Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run migrations

```bash
python manage.py migrate
```

## Create superuser

```bash
python manage.py createsuperuser
```

## Start development server

```bash
python manage.py runserver
```

---

# Testing

Run tests using:

```bash
python manage.py test
```

---

# Future Improvements

- Email notifications
- Search functionality
- Better role-based permissions
- Request approval workflow
- File uploads
- Audit logging
- Advanced filtering and reporting
- Improved frontend UI/UX

---

# Learning Notes

This project was developed as part of learning:
- Django class-based views
- Authentication systems
- CRUD operations
- Database relationships
- Server-side validation
- Template rendering
- URL routing
- Business rule enforcement

---

# Acknowledgements

This project was developed with the assistance of:
- ChatGPT
- Django documentation
- Online programming resources and tutorials

ChatGPT was used as a learning and development aid for understanding Django concepts, debugging issues, and improving project structure/design.

