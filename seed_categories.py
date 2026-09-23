from app import create_app
from app.extensions import db
from app.models.category import Category

app = create_app()

with app.app_context():

    categories = [    #boook category in database 
        "Programming",
        "Database",
        "Artificial Intelligence",
        "Networking",
        "Mathematics"
    ]

    for name in categories:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))

    db.session.commit()

    print("✅ Categories added successfully!")