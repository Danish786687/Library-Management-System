from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template

from config import Config

from app.extensions import (
    db,
    login_manager,
    bcrypt,
    migrate,
    mail,
    limiter,
    cache,
)

from app.models import *
from app.models.user import User
from app.models.setting import Setting

from app.main import main
from app.auth.routes import auth
from app.books import books
from app.categories import categories
from app.students import students
from app.transactions import transactions
from app.settings import settings
from app.users import users
from app.reports import reports


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # -----------------------------
    # Initialize Extensions
    # -----------------------------
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.register_blueprint(
        books,
        url_prefix="/books"
    )

    app.register_blueprint(
        categories,
        url_prefix="/categories"
    )

    app.register_blueprint(
        students,
        url_prefix="/students"
    )

    app.register_blueprint(
        transactions,
        url_prefix="/transactions"
    )

    app.register_blueprint(settings)
    app.register_blueprint(users)
    app.register_blueprint(
        reports,
        url_prefix="/reports"
    )

    # -----------------------------
    # Global Settings
    # -----------------------------
    @app.context_processor
    def inject_settings():

        setting = Setting.query.first()

        if setting is None:
            setting = Setting()

        return dict(setting=setting)

    # -----------------------------
    # Error Handlers
    # -----------------------------
    @app.errorhandler(404)
    def page_not_found(error):

        return render_template(
            "errors/404.html"
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):

        db.session.rollback()

        return render_template(
            "errors/500.html"
        ), 500

    return app