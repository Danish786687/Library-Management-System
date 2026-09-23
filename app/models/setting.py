from app.extensions import db


class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    # Library Information
    library_name = db.Column(
        db.String(100),
        default="Library Management System"
    )

    # Transaction Settings
    default_due_days = db.Column(
        db.Integer,
        default=15
    )

    fine_per_day = db.Column(
        db.Float,
        default=10.0
    )

    allow_manual_due_date = db.Column(
        db.Boolean,
        default=True
    )

    # Book Settings
    low_stock_threshold = db.Column(
        db.Integer,
        default=5
    )

    auto_create_category = db.Column(
        db.Boolean,
        default=True
    )

    # Appearance
    dark_mode = db.Column(
        db.Boolean,
        default=False
    )

    def __repr__(self):
        return "<System Settings>"