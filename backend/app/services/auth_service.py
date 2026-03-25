import re

from ..core.errors import ApiError
from ..extensions import db
from ..models import User
from .audit_service import append_audit_event

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9._-]{3,32}$")


def register_user(payload):
    username = normalize_username(payload.get("username"))
    password = validate_password(payload.get("password"))

    if User.query.filter_by(username=username).first():
        raise ApiError(409, "That username is already taken.")

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.flush()
    db.session.add(
        append_audit_event(
            actor_id=user.id,
            action="auth.registered",
            description="Created a new secure transfer account.",
            subject_type="user",
            subject_id=str(user.id),
        )
    )
    db.session.commit()
    return user


def authenticate_user(payload):
    username = normalize_username(payload.get("username"))
    password = payload.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        raise ApiError(401, "Invalid username or password.")

    db.session.add(
        append_audit_event(
            actor_id=user.id,
            action="auth.logged_in",
            description="Started a new authenticated session.",
            subject_type="user",
            subject_id=str(user.id),
        )
    )
    db.session.commit()
    return user


def get_user_or_404(user_id):
    user = db.session.get(User, user_id)
    if not user:
        raise ApiError(404, "User could not be found.")
    return user


def normalize_username(raw_username):
    username = (raw_username or "").strip().lower()
    if not USERNAME_PATTERN.match(username):
        raise ApiError(
            400,
            "Username must be 3-32 characters and may include letters, numbers, dots, dashes, and underscores.",
        )
    return username


def validate_password(raw_password):
    password = raw_password or ""
    if len(password) < 8:
        raise ApiError(400, "Password must be at least 8 characters long.")
    if len(password) > 128:
        raise ApiError(400, "Password must be 128 characters or fewer.")
    return password
