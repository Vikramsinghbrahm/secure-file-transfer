from flask import Blueprint

from ..utils.responses import success_response

health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/health")
def health_check():
    return success_response(
        data={"status": "ok"},
        message="Secure transfer API is healthy.",
    )
