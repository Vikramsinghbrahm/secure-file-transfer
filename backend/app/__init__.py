import logging
import re
from pathlib import Path
from uuid import uuid4

from flask import Flask, g, request

from .core.config import Config
from .core.errors import register_error_handlers
from .extensions import db, init_extensions


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["STORAGE_ROOT"]).mkdir(parents=True, exist_ok=True)

    configure_logging(app)
    init_extensions(app)
    register_request_hooks(app)

    from .api import register_blueprints

    register_blueprints(app)
    register_error_handlers(app)

    with app.app_context():
        if app.config.get("AUTO_INIT_DB", True):
            db.create_all()

    return app


def configure_logging(app):
    if app.logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    app.logger.setLevel(logging.INFO)


def is_private_network_origin(origin):
    return bool(
        re.match(r"^http://localhost:\d+$", origin or "")
        or re.match(r"^http://127\.0\.0\.1:\d+$", origin or "")
        or re.match(r"^http://192\.168\.\d{1,3}\.\d{1,3}:\d+$", origin or "")
        or re.match(r"^http://10\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$", origin or "")
        or re.match(
            r"^http://172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}:\d+$",
            origin or "",
        )
    )


def is_allowed_origin(app, origin):
    allowed_origins = set(app.config.get("CORS_ALLOWED_ORIGINS", []))

    if origin in allowed_origins:
        return True

    if not origin:
        return False

    if is_private_network_origin(origin):
        return True

    return False


def register_request_hooks(app):
    @app.before_request
    def attach_request_id():
        g.request_id = request.headers.get("X-Request-Id") or uuid4().hex

    @app.before_request
    def handle_preflight():
        if request.method != "OPTIONS":
            return None

        if not request.path.startswith(app.config.get("API_PREFIX", "/api")):
            return None

        if not is_allowed_origin(app, request.headers.get("Origin")):
            return ("", 204)

        return ("", 204)

    @app.after_request
    def harden_response(response):
        origin = request.headers.get("Origin")

        if is_allowed_origin(app, origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = (
                "Authorization, Content-Type, X-Request-Id"
            )
            response.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            )
            response.headers["Access-Control-Expose-Headers"] = (
                "Content-Disposition, X-Request-Id"
            )
            response.headers["Vary"] = "Origin"

        response.headers["X-Request-Id"] = getattr(g, "request_id", uuid4().hex)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response
