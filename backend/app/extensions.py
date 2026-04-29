from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def init_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    register_jwt_callbacks()


def register_jwt_callbacks():
    from .utils.responses import error_response

    @jwt.unauthorized_loader
    def handle_missing_token(message):
        return error_response(message=message, status=401)

    @jwt.invalid_token_loader
    def handle_invalid_token(message):
        return error_response(message=message, status=401)

    @jwt.expired_token_loader
    def handle_expired_token(_, __):
        return error_response(message="Session expired. Sign in again.", status=401)
