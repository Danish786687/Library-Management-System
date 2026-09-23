from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    course = db.Column(db.String(100))

    semester = db.Column(db.String(20))

    phone = db.Column(db.String(15))

    transactions = db.relationship(
        "Transaction",
        backref="student",
        lazy=True
    )

    def __repr__(self):
        return f"<Student {self.name}>"