from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)


# -----------------------
# Add User
# -----------------------
class UserForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("admin", "Admin"),
            ("librarian", "Librarian"),
            ("viewer", "Viewer")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Save User")


# -----------------------
# Edit User
# -----------------------
class EditUserForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    role = SelectField(
        "Role",
        choices=[
            ("admin", "Admin"),
            ("librarian", "Librarian"),
            ("viewer", "Viewer")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Update User")