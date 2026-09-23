from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from app.decorators import admin_required

from app.settings import settings
from app.settings.forms import SettingForm

from app.extensions import db
from app.models.setting import Setting

@settings.route("/", methods=["GET", "POST"])
@login_required
@admin_required
def index():

    setting = Setting.query.first()

    if setting is None:
        setting = Setting()
        db.session.add(setting)
        db.session.commit()

    form = SettingForm(obj=setting)

    if form.validate_on_submit():

        setting.library_name = form.library_name.data
        setting.default_due_days = form.default_due_days.data
        setting.fine_per_day = form.fine_per_day.data
        setting.low_stock_threshold = form.low_stock_threshold.data

        setting.allow_manual_due_date = form.allow_manual_due_date.data
        setting.auto_create_category = form.auto_create_category.data
        setting.dark_mode = form.dark_mode.data

        db.session.commit()

        flash(
            "Settings updated successfully!",
            "success"
        )

        return redirect(url_for("settings.index"))

    return render_template(
        "settings/index.html",
        form=form
    )