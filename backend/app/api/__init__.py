from .auth import auth_blueprint
from .dashboard import dashboard_blueprint
from .files import files_blueprint
from .health import health_blueprint
from .shares import shares_blueprint


def register_blueprints(app):
    prefix = app.config["API_PREFIX"]
    app.register_blueprint(health_blueprint, url_prefix=prefix)
    app.register_blueprint(auth_blueprint, url_prefix=f"{prefix}/auth")
    app.register_blueprint(files_blueprint, url_prefix=f"{prefix}/files")
    app.register_blueprint(dashboard_blueprint, url_prefix=f"{prefix}/dashboard")
    app.register_blueprint(shares_blueprint, url_prefix=f"{prefix}/shares")
