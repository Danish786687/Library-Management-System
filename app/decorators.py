from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        role = (current_user.role or "").lower()

        if role != "admin":

            flash(
                "Access denied. Administrator privileges required.",
                "danger"
            )

            return redirect(url_for("main.dashboard"))

        return func(*args, **kwargs)

    return wrapper


def librarian_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        role = (current_user.role or "").lower()

        if role not in ["admin", "librarian"]:

            flash(
                "Access denied.",
                "danger"
            )

            return redirect(url_for("main.dashboard"))

        return func(*args, **kwargs)

    return wrapper


def viewer_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        role = (current_user.role or "").lower()

        if role not in [
            "admin",
            "librarian",
            "viewer"
        ]:

            flash(
                "Access denied.",
                "danger"
            )

            return redirect(url_for("main.dashboard"))

        return func(*args, **kwargs)

    return wrapper