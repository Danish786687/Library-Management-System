# 📚 Library Management System (LMS)

A robust, modular, full-stack Library Management Web Application built with **Python (Flask)**, implementing Blueprint-based architecture, Object-Relational Mapping (ORM), and relational database migrations.

---

## 🌟 Key Features

* **Modular Architecture:** Structured using Flask Blueprints (`books`, `students`, `transactions`, `users`, `reports`, `settings`).
* **Authentication & Authorization:** Secure user authentication with custom role-based access control using `decorators.py`.
* **Book & Student Management:** Complete CRUD operations for tracking book inventories, student records, and category structures.
* **Transaction Engine:** Efficient tracking for issuing books, processing returns, managing due dates, and logging history.
* **Database Migrations:** Seamless schema management using Flask-Migrate / Alembic (`migrations/`).
* **Database Seeding:** Pre-configured data seeders (`seed.py`, `seed_categories.py`) for quick setup and testing.
* **Reporting & Analytics:** Generate system-level logs and transaction reports.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Flask Framework
* **Database ORM:** Flask-SQLAlchemy
* **Database Migrations:** Flask-Migrate (Alembic)
* **Frontend:** HTML5, CSS3, JavaScript (Jinja2 Templates)
* **Environment Configuration:** Python-dotenv / `config.py`

---

## 📂 Folder Structure

```text
LibraryManagementSystem/
├── app/                 # Core Application Blueprints & Routes
├── books/               # Book & Category Management Modules
├── students/            # Student Record Modules
├── transactions/        # Issue/Return Business Logic
├── users/               # Authentication & User Management
├── settings/            # System Configuration Routes
├── reports/             # Reporting Modules
├── templates/           # HTML Jinja2 Templates
├── static/              # CSS, JS, and Media Assets
├── migrations/          # Alembic DB Migration Files
├── config.py            # Environment Configuration
├── check_db.py          # Database Diagnostics Script
├── debug_db.py          # Database Debugging Script
├── run.py               # Application Entry Point
├── seed.py              # Data Seeding Script
├── seed_categories.py   # Category Seeding Script
└── requirements.txt     # Python Dependencies
