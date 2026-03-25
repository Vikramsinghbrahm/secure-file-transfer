from datetime import UTC, datetime
from uuid import uuid4

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utcnow():
    return datetime.now(UTC).replace(tzinfo=None)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    file_records = db.relationship(
        "FileRecord",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    audit_events = db.relationship(
        "AuditEvent",
        back_populates="actor",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "createdAt": self.created_at.isoformat() + "Z",
        }


class FileRecord(db.Model):
    __tablename__ = "file_records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False, unique=True)
    storage_path = db.Column(db.String(512), nullable=False, unique=True)
    content_type = db.Column(db.String(255), nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)
    sha256_checksum = db.Column(db.String(64), nullable=False)
    download_count = db.Column(db.Integer, nullable=False, default=0)
    last_downloaded_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    owner = db.relationship("User", back_populates="file_records")
    share_links = db.relationship(
        "ShareLink",
        back_populates="file_record",
        cascade="all, delete-orphan",
        order_by="ShareLink.created_at.desc()",
    )

    @property
    def active_share_links(self):
        return [share_link for share_link in self.share_links if share_link.is_active]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.original_filename,
            "contentType": self.content_type,
            "sizeBytes": self.size_bytes,
            "checksumSha256": self.sha256_checksum,
            "downloadCount": self.download_count,
            "lastDownloadedAt": (
                self.last_downloaded_at.isoformat() + "Z"
                if self.last_downloaded_at
                else None
            ),
            "createdAt": self.created_at.isoformat() + "Z",
            "activeShareLinks": [
                share_link.to_dict() for share_link in self.active_share_links
            ],
        }


class AuditEvent(db.Model):
    __tablename__ = "audit_events"

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    action = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    subject_type = db.Column(db.String(64), nullable=True)
    subject_id = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)

    actor = db.relationship("User", back_populates="audit_events")

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action,
            "description": self.description,
            "subjectType": self.subject_type,
            "subjectId": self.subject_id,
            "createdAt": self.created_at.isoformat() + "Z",
        }


class ShareLink(db.Model):
    __tablename__ = "share_links"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    file_id = db.Column(
        db.String(36), db.ForeignKey("file_records.id"), nullable=False, index=True
    )
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    token_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)
    token_preview = db.Column(db.String(24), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    max_downloads = db.Column(db.Integer, nullable=False, default=1)
    download_count = db.Column(db.Integer, nullable=False, default=0)
    last_accessed_at = db.Column(db.DateTime, nullable=True)
    revoked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    file_record = db.relationship("FileRecord", back_populates="share_links")
    creator = db.relationship("User")

    @property
    def is_active(self):
        return (
            self.revoked_at is None
            and self.expires_at > utcnow()
            and self.download_count < self.max_downloads
        )

    @property
    def status(self):
        if self.revoked_at is not None:
            return "revoked"
        if self.expires_at <= utcnow():
            return "expired"
        if self.download_count >= self.max_downloads:
            return "exhausted"
        return "active"

    def to_dict(self):
        return {
            "id": self.id,
            "tokenPreview": self.token_preview,
            "status": self.status,
            "expiresAt": self.expires_at.isoformat() + "Z",
            "maxDownloads": self.max_downloads,
            "downloadCount": self.download_count,
            "lastAccessedAt": (
                self.last_accessed_at.isoformat() + "Z"
                if self.last_accessed_at
                else None
            ),
            "revokedAt": self.revoked_at.isoformat() + "Z" if self.revoked_at else None,
            "createdAt": self.created_at.isoformat() + "Z",
        }

    def to_created_dict(self, share_url):
        payload = self.to_dict()
        payload["shareUrl"] = share_url
        return payload
