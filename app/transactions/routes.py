from datetime import datetime, timedelta, date

from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app.transactions import transactions
from app.transactions.forms import TransactionForm

from app.extensions import db

from app.models.student import Student
from app.models.book import Book
from app.models.transaction import Transaction
from app.models.setting import Setting


# -----------------------------
# View Transactions
# -----------------------------
@transactions.route("/")
@login_required
def index():

    transactions_list = Transaction.query.order_by(
        Transaction.id.desc()
    ).all()

    today = datetime.utcnow()

    setting = Setting.query.first()

    fine_per_day = (
        setting.fine_per_day
        if setting
        else 5
    )

    for transaction in transactions_list:

        if transaction.status == "Issued":

            if today > transaction.due_date:

                late_days = (
                    today - transaction.due_date
                ).days

                transaction.current_fine = (
                    late_days * fine_per_day
                )

                transaction.overdue = True

            else:

                transaction.current_fine = 0

                transaction.overdue = False

        else:

            transaction.current_fine = transaction.fine

            transaction.overdue = False

    return render_template(
        "transactions/index.html",
        transactions=transactions_list
    )


# -----------------------------
# Issue Book
# -----------------------------
@transactions.route("/issue", methods=["GET", "POST"])
@login_required
def issue_book():

    form = TransactionForm()

    form.student.choices = [
        (s.id, f"{s.student_id} - {s.name}")
        for s in Student.query.order_by(Student.name).all()
    ]

    form.book.choices = [
        (b.id, b.title)
        for b in Book.query.filter(Book.available > 0).all()
    ]

    if form.validate_on_submit():

        book = Book.query.get(form.book.data)

        if book.available <= 0:

            flash(
                "Book is not available.",
                "danger"
            )

            return redirect(
                url_for("transactions.issue_book")
            )

        # -----------------------------
        # Manual Due Date
        # -----------------------------
        if form.due_date.data:

            if form.due_date.data < date.today():

                flash(
                    "Due date cannot be in the past.",
                    "danger"
                )

                return render_template(
                    "transactions/issue_book.html",
                    form=form,
                    today=date.today().isoformat()
                )

            due_date = datetime.combine(
                form.due_date.data,
                datetime.min.time()
            )

        # -----------------------------
        # Default Due Date from Settings
        # -----------------------------
        else:

            setting = Setting.query.first()

            due_days = (
                setting.default_due_days
                if setting
                else 15
            )

            due_date = (
                datetime.utcnow()
                + timedelta(days=due_days)
            )

        transaction = Transaction(

            student_id=form.student.data,

            book_id=form.book.data,

            issue_date=datetime.utcnow(),

            due_date=due_date,

            status="Issued"

        )

        book.available -= 1

        db.session.add(transaction)

        db.session.commit()

        flash(
            "Book issued successfully!",
            "success"
        )

        return redirect(
            url_for("transactions.index")
        )

    return render_template(
        "transactions/issue_book.html",
        form=form,
        today=date.today().isoformat()
    )


# -----------------------------
# Return Book
# -----------------------------
@transactions.route("/return/<int:transaction_id>")
@login_required
def return_book(transaction_id):

    transaction = Transaction.query.get_or_404(
        transaction_id
    )

    if transaction.status == "Returned":

        flash(
            "Book already returned.",
            "warning"
        )

        return redirect(
            url_for("transactions.index")
        )

    transaction.status = "Returned"

    transaction.return_date = datetime.utcnow()

    transaction.book.available += 1

    setting = Setting.query.first()

    fine_per_day = (
        setting.fine_per_day
        if setting
        else 5
    )

    late_days = (
        transaction.return_date -
        transaction.due_date
    ).days

    if late_days > 0:

        transaction.fine = (
            late_days * fine_per_day
        )

    else:

        transaction.fine = 0

    db.session.commit()

    flash(
        "Book returned successfully!",
        "success"
    )

    return redirect(
        url_for("transactions.index")
    )

    transaction = Transaction.query.get_or_404(transaction_id)

    if transaction.status == "Returned":
        flash("Book already returned.", "warning")
        return redirect(url_for("transactions.index"))

    today = datetime.utcnow()

    transaction.return_date = today
    transaction.status = "Returned"

    # Calculate fine
    fine_per_day = 5

    if today > transaction.due_date:

        late_days = (today - transaction.due_date).days

        transaction.fine = late_days * fine_per_day

    else:

        transaction.fine = 0

    # Increase available books
    transaction.book.available += 1

    db.session.commit()

    flash(
        f"Book returned successfully. Fine: ₹{transaction.fine}",
        "success"
    )

    return redirect(url_for("transactions.index"))