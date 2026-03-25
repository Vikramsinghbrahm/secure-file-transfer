from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..services.auth_service import get_user_or_404
from ..services.file_service import (
    delete_file_for_user,
    get_download_payload,
    list_files_for_user,
    store_file_for_user,
    stream_file_response,
)
from ..services.rate_limit_service import get_client_ip, rate_limit
from ..services.share_service import create_share_link_for_user
from ..utils.responses import success_response

files_blueprint = Blueprint("files", __name__)


def build_upload_rate_limit_key():
    return f"upload:{get_client_ip()}:{get_jwt_identity()}"


@files_blueprint.get("")
@jwt_required()
def list_files():
    user_id = int(get_jwt_identity())
    files = [file_record.to_dict() for file_record in list_files_for_user(user_id)]
    return success_response(
        data={"files": files},
        message="Files fetched successfully.",
    )


@files_blueprint.post("")
@jwt_required()
@rate_limit(
    limit_config_key="UPLOAD_RATE_LIMIT_REQUESTS",
    window_config_key="UPLOAD_RATE_LIMIT_WINDOW_SECONDS",
    key_func=build_upload_rate_limit_key,
    message="Upload rate limit exceeded. Please wait before sending more files.",
)
def upload_file():
    user = get_user_or_404(int(get_jwt_identity()))
    file_record = store_file_for_user(
        user=user,
        uploaded_file=request.files.get("file"),
        storage_root=current_app.config["STORAGE_ROOT"],
    )
    return success_response(
        data={"file": file_record.to_dict()},
        message="File uploaded successfully.",
        status=201,
    )


@files_blueprint.get("/<file_id>/download")
@jwt_required()
def download_file(file_id):
    payload = get_download_payload(
        user_id=int(get_jwt_identity()),
        file_id=file_id,
        storage_root=current_app.config["STORAGE_ROOT"],
    )
    return stream_file_response(
        file_path=payload["path"],
        download_name=payload["file"].original_filename,
        content_type=payload["file"].content_type,
        chunk_size=current_app.config["DOWNLOAD_CHUNK_SIZE_BYTES"],
    )


@files_blueprint.delete("/<file_id>")
@jwt_required()
def delete_file(file_id):
    delete_file_for_user(
        user_id=int(get_jwt_identity()),
        file_id=file_id,
        storage_root=current_app.config["STORAGE_ROOT"],
    )
    return success_response(message="File deleted successfully.")


@files_blueprint.post("/<file_id>/shares")
@jwt_required()
def create_share_link(file_id):
    payload = request.get_json(silent=True) or {}
    share_link = create_share_link_for_user(
        user_id=int(get_jwt_identity()),
        file_id=file_id,
        payload=payload,
        api_prefix=current_app.config["API_PREFIX"],
        base_url=current_app.config["PUBLIC_BASE_URL"] or request.url_root.rstrip("/"),
        default_ttl_minutes=current_app.config["DEFAULT_SHARE_LINK_TTL_MINUTES"],
        max_ttl_minutes=current_app.config["MAX_SHARE_LINK_TTL_MINUTES"],
        default_max_downloads=current_app.config["DEFAULT_SHARE_LINK_MAX_DOWNLOADS"],
        max_share_downloads=current_app.config["MAX_SHARE_LINK_MAX_DOWNLOADS"],
    )
    return success_response(
        data={"shareLink": share_link},
        message="Expiring share link created successfully.",
        status=201,
    )
