from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired, NumberRange


class SettingForm(FlaskForm):

    library_name = StringField(
        "Library Name",
        validators=[DataRequired()]
    )

    default_due_days = IntegerField(
        "Default Due Days",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=365)
        ]
    )

    fine_per_day = FloatField(
        "Fine Per Day (₹)",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    low_stock_threshold = IntegerField(
        "Low Stock Alert",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    allow_manual_due_date = BooleanField(
        "Allow Manual Due Date"
    )

    auto_create_category = BooleanField(
        "Auto Create Categories"
    )

    dark_mode = BooleanField(
        "Enable Dark Mode"
    )

    submit = SubmitField("💾 Save Settings")