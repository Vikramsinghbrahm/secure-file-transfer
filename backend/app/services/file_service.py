import hashlib
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

from flask import Response, stream_with_context
from sqlalchemy.orm import selectinload
from werkzeug.utils import secure_filename

from ..core.errors import ApiError
from ..extensions import db
from ..models import FileRecord
from .audit_service import append_audit_event


def list_files_for_user(user_id):
    return (
        FileRecord.query.options(selectinload(FileRecord.share_links))
        .filter_by(owner_id=user_id)
        .order_by(FileRecord.created_at.desc())
        .all()
    )


def store_file_for_user(user, uploaded_file, storage_root):
    if uploaded_file is None:
        raise ApiError(400, "Attach a file before uploading.")

    original_filename = (uploaded_file.filename or "").strip()
    if not original_filename:
        raise ApiError(400, "The uploaded file is missing a filename.")

    safe_filename = secure_filename(original_filename)
    if not safe_filename:
        raise ApiError(400, "Filename contains unsupported characters.")

    user_directory = Path(storage_root) / str(user.id)
    user_directory.mkdir(parents=True, exist_ok=True)

    stored_filename = f"{uuid4().hex}-{safe_filename}"
    destination = user_directory / stored_filename

    sha256 = hashlib.sha256()
    total_size = 0

    try:
        with destination.open("wb") as handle:
            while True:
                chunk = uploaded_file.stream.read(1024 * 1024)
                if not chunk:
                    break
                total_size += len(chunk)
                sha256.update(chunk)
                handle.write(chunk)

        if total_size == 0:
            destination.unlink(missing_ok=True)
            raise ApiError(400, "Empty files are not supported.")

        record = FileRecord(
            original_filename=original_filename,
            stored_filename=stored_filename,
            storage_path=str(destination.relative_to(storage_root)),
            content_type=uploaded_file.mimetype or "application/octet-stream",
            size_bytes=total_size,
            sha256_checksum=sha256.hexdigest(),
            owner_id=user.id,
        )

        db.session.add(record)
        db.session.flush()
        db.session.add(
            append_audit_event(
                actor_id=user.id,
                action="file.uploaded",
                description=f"Uploaded {original_filename}.",
                subject_type="file",
                subject_id=record.id,
            )
        )
        db.session.commit()
        return record
    except ApiError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        destination.unlink(missing_ok=True)
        raise


def get_download_payload(user_id, file_id, storage_root):
    file_record = get_owned_file(user_id, file_id)
    absolute_path = resolve_storage_path(storage_root, file_record.storage_path)

    if not absolute_path.exists():
        raise ApiError(404, "Stored file is no longer available.")

    file_record.download_count += 1
    file_record.last_downloaded_at = datetime.now(UTC).replace(tzinfo=None)
    db.session.add(
        append_audit_event(
            actor_id=user_id,
            action="file.downloaded",
            description=f"Downloaded {file_record.original_filename}.",
            subject_type="file",
            subject_id=file_record.id,
        )
    )
    db.session.commit()

    return {"file": file_record, "path": absolute_path}


def delete_file_for_user(user_id, file_id, storage_root):
    file_record = get_owned_file(user_id, file_id)
    absolute_path = resolve_storage_path(storage_root, file_record.storage_path)

    if absolute_path.exists():
        absolute_path.unlink()

    db.session.delete(file_record)
    db.session.add(
        append_audit_event(
            actor_id=user_id,
            action="file.deleted",
            description=f"Deleted {file_record.original_filename}.",
            subject_type="file",
            subject_id=file_record.id,
        )
    )
    db.session.commit()


def get_owned_file(user_id, file_id):
    file_record = FileRecord.query.filter_by(id=file_id, owner_id=user_id).first()
    if not file_record:
        raise ApiError(404, "File could not be found for this user.")
    return file_record


def resolve_storage_path(storage_root, relative_path):
    return Path(storage_root) / relative_path


def stream_file_response(file_path, download_name, content_type, chunk_size):
    response = Response(
        stream_with_context(iter_file_chunks(file_path, chunk_size)),
        mimetype=content_type,
    )
    response.headers["Content-Length"] = str(file_path.stat().st_size)
    response.headers["Content-Disposition"] = build_content_disposition(download_name)
    response.headers["X-Accel-Buffering"] = "no"
    return response


def iter_file_chunks(file_path, chunk_size):
    with file_path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            yield chunk


def build_content_disposition(download_name):
    safe_ascii_name = secure_filename(download_name) or "download.bin"
    encoded_name = quote(download_name)
    return (
        f"attachment; filename=\"{safe_ascii_name}\"; "
        f"filename*=UTF-8''{encoded_name}"
    )
