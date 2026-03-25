from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from ..services.auth_service import authenticate_user, register_user
from ..services.rate_limit_service import get_client_ip, rate_limit
from ..utils.responses import success_response

auth_blueprint = Blueprint("auth", __name__)


def build_login_rate_limit_key():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip().lower() or "anonymous"
    return f"login:{get_client_ip()}:{username}"


@auth_blueprint.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    user = register_user(payload)
    token = create_access_token(identity=str(user.id))
    return success_response(
        data={"token": token, "user": user.to_dict()},
        message="Account created successfully.",
        status=201,
    )


@auth_blueprint.post("/login")
@rate_limit(
    limit_config_key="LOGIN_RATE_LIMIT_ATTEMPTS",
    window_config_key="LOGIN_RATE_LIMIT_WINDOW_SECONDS",
    key_func=build_login_rate_limit_key,
    message="Too many login attempts. Please wait before trying again.",
)
def login():
    payload = request.get_json(silent=True) or {}
    user = authenticate_user(payload)
    token = create_access_token(identity=str(user.id))
    return success_response(
        data={"token": token, "user": user.to_dict()},
        message="Login successful.",
    )
