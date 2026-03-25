from sqlalchemy import func

from ..extensions import db
from ..models import AuditEvent, FileRecord, ShareLink, utcnow


def build_dashboard_snapshot(user_id):
    total_files = (
        db.session.query(func.count(FileRecord.id))
        .filter(FileRecord.owner_id == user_id)
        .scalar()
        or 0
    )
    total_storage = (
        db.session.query(func.coalesce(func.sum(FileRecord.size_bytes), 0))
        .filter(FileRecord.owner_id == user_id)
        .scalar()
        or 0
    )
    total_downloads = (
        db.session.query(func.coalesce(func.sum(FileRecord.download_count), 0))
        .filter(FileRecord.owner_id == user_id)
        .scalar()
        or 0
    )
    active_shares = (
        db.session.query(func.count(ShareLink.id))
        .join(FileRecord, ShareLink.file_id == FileRecord.id)
        .filter(FileRecord.owner_id == user_id)
        .filter(ShareLink.revoked_at.is_(None))
        .filter(ShareLink.expires_at > utcnow())
        .filter(ShareLink.download_count < ShareLink.max_downloads)
        .scalar()
        or 0
    )
    recent_files = (
        FileRecord.query.filter_by(owner_id=user_id)
        .order_by(FileRecord.created_at.desc())
        .limit(5)
        .all()
    )
    activity = (
        AuditEvent.query.filter_by(actor_id=user_id)
        .order_by(AuditEvent.created_at.desc())
        .limit(8)
        .all()
    )

    return {
        "metrics": {
            "totalFiles": total_files,
            "storageBytes": total_storage,
            "downloadCount": total_downloads,
            "activeShares": active_shares,
        },
        "recentFiles": [file_record.to_dict() for file_record in recent_files],
        "activity": [event.to_dict() for event in activity],
    }
