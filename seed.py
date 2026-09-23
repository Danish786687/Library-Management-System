from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User

#admin create user generate script

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email="admin@library.com").first()  #check duplicacy #database queryy >> to store info of user
    if not admin:
        admin = User(
            name="Administrator",           #admiin exist or not0
            email="admin@library.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),  #password saved in encrpyted way(not in simple way)
            role="admin"
        )

        db.session.add(admin)  
        db.session.commit()

        print("✅ Admin user created successfully!")

    else:
        print("ℹ️ Admin user already exists.")