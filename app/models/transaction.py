from datetime import datetime
from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id"),
        nullable=False
    )

    issue_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    due_date = db.Column(db.DateTime)

    return_date = db.Column(db.DateTime)

    fine = db.Column(
        db.Float,
        default=0.0
    )

    status = db.Column(
        db.String(20),
        default="Issued"
    )

    def __repr__(self):
        return f"<Transaction {self.id}>"