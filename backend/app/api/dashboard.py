from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..services.auth_service import get_user_or_404
from ..services.dashboard_service import build_dashboard_snapshot
from ..utils.responses import success_response

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.get("")
@jwt_required()
def get_dashboard():
    user = get_user_or_404(int(get_jwt_identity()))
    snapshot = build_dashboard_snapshot(user.id)
    return success_response(
        data=snapshot,
        message=f"Workspace loaded for {user.username}.",
    )
