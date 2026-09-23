from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import or_

from app.books import books
from app.books.forms import BookForm

from app.extensions import db
from app.models.book import Book
from app.models.category import Category


# ---------------------------------
# View All Books
# ---------------------------------
@books.route("/")
@login_required
def index():

    search = request.args.get("search", "")

    books_query = Book.query

    if search:

        books_query = books_query.join(Category).filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Category.name.ilike(f"%{search}%")
            )
        )

    books_list = books_query.order_by(Book.id.desc()).all()

    return render_template(
        "books/index.html",
        books=books_list,
        search=search
    )


# ---------------------------------
# Add Book
# ---------------------------------
@books.route("/add", methods=["GET", "POST"])
@login_required
def add_book():

    form = BookForm()

    # Existing Categories
    form.category.choices = [(0, "-- Select Existing Category --")]

    form.category.choices += [
        (c.id, c.name)
        for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():

        # -----------------------------
        # If user entered a new category
        # -----------------------------
        if form.new_category.data and form.new_category.data.strip():

            # Remove extra spaces and convert nicely
            category_name = " ".join(
                form.new_category.data.split()
            ).title()

            # Case-insensitive search
            category = Category.query.filter(
                db.func.lower(Category.name) == category_name.lower()
            ).first()

            # Create category if it doesn't exist
            if category is None:

                category = Category(
                    name=category_name
                )

                db.session.add(category)
                db.session.commit()

            category_id = category.id

        # -----------------------------
        # Existing category selected
        # -----------------------------
        elif form.category.data != 0:

            category_id = form.category.data

        # -----------------------------
        # Nothing selected
        # -----------------------------
        else:

            flash(
                "Please select an existing category or enter a new one.",
                "danger"
            )

            return redirect(url_for("books.add_book"))

        # -----------------------------
        # Save Book
        # -----------------------------
        book = Book(
            title=form.title.data,
            author=form.author.data,
            category_id=category_id,
            quantity=form.quantity.data,
            available=form.quantity.data
        )

        db.session.add(book)
        db.session.commit()

        flash(
            "Book added successfully!",
            "success"
        )

        return redirect(url_for("books.index"))

    return render_template(
        "books/add_book.html",
        form=form
    )


# ---------------------------------
# Edit Book
# ---------------------------------
@books.route("/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):

    book = Book.query.get_or_404(book_id)

    form = BookForm()

    form.category.choices = [
        (c.id, c.name)
        for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():

        book.title = form.title.data
        book.author = form.author.data
        book.category_id = form.category.data

        old_quantity = book.quantity
        old_available = book.available

        book.quantity = form.quantity.data

        difference = form.quantity.data - old_quantity
        book.available = old_available + difference

        if book.available < 0:
            book.available = 0

        db.session.commit()

        flash(
            "Book updated successfully!",
            "success"
        )

        return redirect(url_for("books.index"))

    form.title.data = book.title
    form.author.data = book.author
    form.category.data = book.category_id
    form.quantity.data = book.quantity

    return render_template(
        "books/edit_book.html",
        form=form
    )


# ---------------------------------
# Delete Book
# ---------------------------------
@books.route("/delete/<int:book_id>")
@login_required
def delete_book(book_id):

    book = Book.query.get_or_404(book_id)

    if book.transactions:

        flash(
            "Cannot delete this book because transaction records exist.",
            "danger"
        )

        return redirect(url_for("books.index"))

    db.session.delete(book)
    db.session.commit()

    flash(
        "Book deleted successfully!",
        "success"
    )

    return redirect(url_for("books.index"))