from app.extensions import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    author = db.Column(db.String(100), nullable=False)

    isbn = db.Column(db.String(20), unique=True)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    quantity = db.Column(db.Integer, default=1)

    available = db.Column(db.Integer, default=1)

    cover_image = db.Column(db.String(255))

    transactions = db.relationship(
        "Transaction",
        backref="book",
        lazy=True
    )

    def __repr__(self):
        return f"<Book {self.title}>"