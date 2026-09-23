from flask_wtf import FlaskForm

from wtforms import (
    SelectField,
    DateField,
    SubmitField
)

from wtforms.validators import DataRequired, Optional


class TransactionForm(FlaskForm):

    student = SelectField(
        "Student",
        coerce=int,
        validators=[DataRequired()]
    )

    book = SelectField(
        "Book",
        coerce=int,
        validators=[DataRequired()]
    )

    due_date = DateField(
    "Due Date",
    format="%Y-%m-%d",
    validators=[Optional()]
    )
    
    submit = SubmitField("Issue Book")