from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField
)
from wtforms.validators import DataRequired, Email

#

class StudentForm(FlaskForm):

    student_id = StringField(
        "Student ID",
        validators=[DataRequired()]
    )

    name = StringField(
        "Student Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    course = StringField(
        "Course",
        validators=[DataRequired()]
    )

    semester = StringField(
        "Semester",
        validators=[DataRequired()]
    )

    phone = StringField(
        "Phone Number",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Student")