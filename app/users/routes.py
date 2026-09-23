from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import func

from app.decorators import admin_required
from app.users import users
from app.users.forms import (
    UserForm,
    EditUserForm
)
from app.users.reset_password_form import ResetPasswordForm

from app.extensions import db, bcrypt

from app.models.user import User


# ------------------------------------
# View Users
# ------------------------------------
@users.route("/")
@login_required
@admin_required
def index():

    users_list = User.query.order_by(
        User.id.asc()
    ).all()

    return render_template(
        "users/index.html",
        users=users_list
    )


# ------------------------------------
# Add User
# ------------------------------------
@users.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():

    form = UserForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("users.add_user")
            )

        password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=password,
            role=form.role.data.lower()
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect(
            url_for("users.index")
        )

    return render_template(
        "users/add_user.html",
        form=form
    )


# ------------------------------------
# Edit User
# ------------------------------------
@users.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):

    user = User.query.get_or_404(user_id)

    form = EditUserForm()

    if form.validate_on_submit():

        existing = User.query.filter(
            User.email == form.email.data,
            User.id != user.id
        ).first()

        if existing:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "users.edit_user",
                    user_id=user.id
                )
            )

        user.name = form.name.data
        user.email = form.email.data
        user.role = form.role.data.lower()

        db.session.commit()

        flash(
            "User updated successfully.",
            "success"
        )

        return redirect(
            url_for("users.index")
        )

    form.name.data = user.name
    form.email.data = user.email
    form.role.data = user.role.lower()

    return render_template(
        "users/edit_user.html",
        form=form
    )


# ------------------------------------
# Delete User
# ------------------------------------
@users.route("/delete/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "danger"
        )

        return redirect(
            url_for("users.index")
        )

    admin_count = User.query.filter(
        func.lower(User.role) == "admin"
    ).count()

    if (
        user.role.lower() == "admin"
        and admin_count <= 1
    ):

        flash(
            "Cannot delete the last administrator.",
            "danger"
        )

        return redirect(
            url_for("users.index")
        )

    db.session.delete(user)
    db.session.commit()

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect(
        url_for("users.index")
    )


# ------------------------------------
# Reset Password
# ------------------------------------
@users.route(
    "/reset-password/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def reset_password(user_id):

    user = User.query.get_or_404(user_id)

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        db.session.commit()

        flash(
            "Password reset successfully.",
            "success"
        )

        return redirect(
            url_for("users.index")
        )

    return render_template(
        "users/reset_password.html",
        form=form,
        user=user
    )