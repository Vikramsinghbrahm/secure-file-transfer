import hashlib
import secrets
from datetime import timedelta

from ..core.errors import ApiError
from ..extensions import db
from ..models import FileRecord, ShareLink, utcnow
from .audit_service import append_audit_event
from .file_service import get_owned_file, resolve_storage_path


def create_share_link_for_user(
    user_id,
    file_id,
    payload,
    *,
    api_prefix,
    base_url,
    default_ttl_minutes,
    max_ttl_minutes,
    default_max_downloads,
    max_share_downloads,
):
    file_record = get_owned_file(user_id, file_id)
    expires_in_minutes = parse_positive_int(
        payload.get("expiresInMinutes"),
        default=default_ttl_minutes,
        maximum=max_ttl_minutes,
        field_name="expiresInMinutes",
    )
    max_downloads = parse_positive_int(
        payload.get("maxDownloads"),
        default=default_max_downloads,
        maximum=max_share_downloads,
        field_name="maxDownloads",
    )

    raw_token = secrets.token_urlsafe(32)
    share_link = ShareLink(
        file_id=file_record.id,
        creator_id=user_id,
        token_hash=hash_share_token(raw_token),
        token_preview=f"{raw_token[:6]}...{raw_token[-4:]}",
        expires_at=utcnow() + timedelta(minutes=expires_in_minutes),
        max_downloads=max_downloads,
    )

    db.session.add(share_link)
    db.session.flush()
    db.session.add(
        append_audit_event(
            actor_id=user_id,
            action="share.created",
            description=f"Generated an expiring share link for {file_record.original_filename}.",
            subject_type="share_link",
            subject_id=share_link.id,
        )
    )
    db.session.commit()

    share_url = build_share_url(base_url, api_prefix, raw_token)
    return share_link.to_created_dict(share_url)


def revoke_share_link_for_user(user_id, share_link_id):
    share_link = (
        ShareLink.query.join(FileRecord, ShareLink.file_id == FileRecord.id)
        .filter(ShareLink.id == share_link_id)
        .filter(FileRecord.owner_id == user_id)
        .first()
    )
    if not share_link:
        raise ApiError(404, "Share link could not be found for this user.")

    if share_link.revoked_at is None:
        share_link.revoked_at = utcnow()
        db.session.add(
            append_audit_event(
                actor_id=user_id,
                action="share.revoked",
                description=f"Revoked share access for {share_link.file_record.original_filename}.",
                subject_type="share_link",
                subject_id=share_link.id,
            )
        )
        db.session.commit()


def resolve_share_download(token, storage_root):
    share_link = ShareLink.query.filter_by(token_hash=hash_share_token(token)).first()
    if not share_link:
        raise ApiError(404, "Share link could not be found.")
    if share_link.revoked_at is not None:
        raise ApiError(410, "Share link has been revoked.")
    if share_link.expires_at <= utcnow():
        raise ApiError(410, "Share link has expired.")
    if share_link.download_count >= share_link.max_downloads:
        raise ApiError(410, "Share link download limit has been reached.")

    absolute_path = resolve_storage_path(storage_root, share_link.file_record.storage_path)
    if not absolute_path.exists():
        raise ApiError(404, "Stored file is no longer available.")

    share_link.download_count += 1
    share_link.last_accessed_at = utcnow()
    share_link.file_record.download_count += 1
    share_link.file_record.last_downloaded_at = utcnow()

    db.session.add(
        append_audit_event(
            actor_id=share_link.creator_id,
            action="share.downloaded",
            description=f"External recipient downloaded {share_link.file_record.original_filename}.",
            subject_type="share_link",
            subject_id=share_link.id,
        )
    )
    db.session.commit()

    return {
        "file": share_link.file_record,
        "path": absolute_path,
        "shareLink": share_link,
    }


def build_share_url(base_url, api_prefix, raw_token):
    normalized_base_url = base_url.rstrip("/")
    return f"{normalized_base_url}{api_prefix}/shares/{raw_token}/download"


def hash_share_token(raw_token):
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def parse_positive_int(raw_value, *, default, maximum, field_name):
    if raw_value in (None, ""):
        return default

    try:
        parsed = int(raw_value)
    except (TypeError, ValueError) as error:
        raise ApiError(400, f"{field_name} must be a positive integer.") from error

    if parsed < 1 or parsed > maximum:
        raise ApiError(400, f"{field_name} must be between 1 and {maximum}.")

    return parsed
