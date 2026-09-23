import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "library_management_secret_key_2026"
    )

    SQLALCHEMY_DATABASE_URI = (
    os.environ.get("DATABASE_URL")
    or "sqlite:///" + os.path.join(BASE_DIR, "library.db")

    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "app",
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024