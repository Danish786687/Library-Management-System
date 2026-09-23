from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db

from app.models.book import Book
from app.models.student import Student
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.setting import Setting

main = Blueprint("main", __name__)


# ---------------------------------
# Home Page
# ---------------------------------
@main.route("/")
def home():
    return render_template("index.html")


# ---------------------------------
# Dashboard
# ---------------------------------
@main.route("/dashboard")
@login_required
def dashboard():

    # -----------------------------
    # Basic Statistics
    # -----------------------------
    total_books = Book.query.count()

    total_students = Student.query.count()

    total_categories = Category.query.count()

    books_issued = Transaction.query.filter_by(
        status="Issued"
    ).count()

    books_returned = Transaction.query.filter_by(
        status="Returned"
    ).count()

    # -----------------------------
    # Overdue Books
    # -----------------------------
    today = datetime.utcnow()

    overdue_books = Transaction.query.filter(
        Transaction.status == "Issued",
        Transaction.due_date < today
    ).count()

    # -----------------------------
    # Low Stock Books
    # -----------------------------
    setting = Setting.query.first()

    threshold = (
        setting.low_stock_threshold
        if setting
        else 5
    )

    low_stock_books = Book.query.filter(
        Book.available <= threshold
    ).count()

    # -----------------------------
    # Total Fine Collected
    # -----------------------------
    total_fine = db.session.query(
        func.sum(Transaction.fine)
    ).scalar()

    if total_fine is None:
        total_fine = 0
    # -----------------------------
    # Books by Category
    # -----------------------------
    category_data = (
        db.session.query(
            Category.name,
            func.count(Book.id)
        )
        .outerjoin(Book)
        .group_by(Category.id)
        .all()
    )
    
    category_labels = [item[0] for item in category_data]
    category_counts = [item[1] for item in category_data]

    return render_template(
    "dashboard.html",
    total_books=total_books,
    total_students=total_students,
    total_categories=total_categories,
    books_issued=books_issued,
    books_returned=books_returned,
    overdue_books=overdue_books,
    low_stock_books=low_stock_books,
    total_fine=total_fine,
    category_labels=category_labels,
    category_counts=category_counts
)