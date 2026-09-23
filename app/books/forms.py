from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, NumberRange, Optional


class BookForm(FlaskForm):

    title = StringField(
        "Book Title",
        validators=[DataRequired()]
    )

    author = StringField(
        "Author",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Existing Category",
        coerce=int,
        validators=[Optional()]
    )

    new_category = StringField(
        "New Category (Optional)",
        validators=[Optional()]
    )

    quantity = IntegerField(
        "Quantity",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    submit = SubmitField("Save Book")