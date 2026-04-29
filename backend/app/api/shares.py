from flask import Blueprint, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..services.encryption_service import get_fernet
from ..services.file_service import stream_file_response
from ..services.share_service import resolve_share_download, revoke_share_link_for_user
from ..utils.responses import success_response

shares_blueprint = Blueprint("shares", __name__)


@shares_blueprint.get("/<token>/download")
def download_from_share_link(token):
    payload = resolve_share_download(
        token=token,
        storage_root=current_app.config["STORAGE_ROOT"],
    )
    file_record = payload["file"]
    fernet = get_fernet(current_app) if file_record.encrypted else None
    return stream_file_response(
        file_path=payload["path"],
        download_name=file_record.original_filename,
        content_type=file_record.content_type,
        chunk_size=current_app.config["DOWNLOAD_CHUNK_SIZE_BYTES"],
        fernet=fernet,
        content_length=file_record.size_bytes if fernet else None,
    )


@shares_blueprint.delete("/<share_link_id>")
@jwt_required()
def revoke_share_link(share_link_id):
    revoke_share_link_for_user(
        user_id=int(get_jwt_identity()),
        share_link_id=share_link_id,
    )
    return success_response(message="Share link revoked successfully.")
