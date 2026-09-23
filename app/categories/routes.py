from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.categories import categories
from app.categories.forms import CategoryForm

from app.extensions import db
from app.models.category import Category


# ---------------------------------
# View Categories
# ---------------------------------
@categories.route("/")
@login_required
def index():

    search = request.args.get("search", "")

    categories_query = Category.query

    if search:
        categories_query = categories_query.filter(
            Category.name.ilike(f"%{search}%")
        )

    categories_list = categories_query.order_by(Category.name).all()

    return render_template(
        "categories/index.html",
        categories=categories_list,
        search=search
    )


# ---------------------------------
# Add Category
# ---------------------------------
@categories.route("/add", methods=["GET", "POST"])
@login_required
def add_category():

    form = CategoryForm()

    if form.validate_on_submit():

        category_name = " ".join(
            form.name.data.split()
        ).title()

        existing = Category.query.filter(
            db.func.lower(Category.name) == category_name.lower()
        ).first()

        if existing:

            flash(
                "Category already exists.",
                "warning"
            )

            return redirect(url_for("categories.add_category"))

        category = Category(
            name=category_name
        )

        db.session.add(category)
        db.session.commit()

        flash(
            "Category added successfully!",
            "success"
        )

        return redirect(url_for("categories.index"))

    return render_template(
        "categories/add_category.html",
        form=form
    )


# ---------------------------------
# Edit Category
# ---------------------------------
@categories.route("/edit/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):

    category = Category.query.get_or_404(category_id)

    form = CategoryForm()

    if form.validate_on_submit():

        category_name = " ".join(
            form.name.data.split()
        ).title()

        duplicate = Category.query.filter(
            db.func.lower(Category.name) == category_name.lower(),
            Category.id != category.id
        ).first()

        if duplicate:

            flash(
                "Another category with this name already exists.",
                "warning"
            )

            return redirect(
                url_for(
                    "categories.edit_category",
                    category_id=category.id
                )
            )

        category.name = category_name

        db.session.commit()

        flash(
            "Category updated successfully!",
            "success"
        )

        return redirect(url_for("categories.index"))

    form.name.data = category.name

    return render_template(
        "categories/edit_category.html",
        form=form
    )


# ---------------------------------
# Delete Category
# ---------------------------------
@categories.route("/delete/<int:category_id>")
@login_required
def delete_category(category_id):

    category = Category.query.get_or_404(category_id)

    if category.books:

        flash(
            "Cannot delete category because books exist in it.",
            "danger"
        )

        return redirect(url_for("categories.index"))

    db.session.delete(category)
    db.session.commit()

    flash(
        "Category deleted successfully!",
        "success"
    )

    return redirect(url_for("categories.index"))