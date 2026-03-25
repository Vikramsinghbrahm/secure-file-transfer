import os
from datetime import timedelta
from pathlib import Path


def read_int_env(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


BASE_DIR = Path(__file__).resolve().parents[2]
INSTANCE_DIR = BASE_DIR / "instance"


class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "local-development-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "local-jwt-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(INSTANCE_DIR / 'secure_transfer.db').as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=read_int_env("JWT_ACCESS_TOKEN_MINUTES", 60)
    )
    MAX_CONTENT_LENGTH = read_int_env("MAX_CONTENT_LENGTH_MB", 25) * 1024 * 1024
    STORAGE_ROOT = Path(os.getenv("STORAGE_ROOT", INSTANCE_DIR / "storage"))
    DOWNLOAD_CHUNK_SIZE_BYTES = read_int_env("DOWNLOAD_CHUNK_SIZE_BYTES", 64 * 1024)
    DEFAULT_SHARE_LINK_TTL_MINUTES = read_int_env("DEFAULT_SHARE_LINK_TTL_MINUTES", 15)
    MAX_SHARE_LINK_TTL_MINUTES = read_int_env("MAX_SHARE_LINK_TTL_MINUTES", 24 * 60)
    DEFAULT_SHARE_LINK_MAX_DOWNLOADS = read_int_env(
        "DEFAULT_SHARE_LINK_MAX_DOWNLOADS", 1
    )
    MAX_SHARE_LINK_MAX_DOWNLOADS = read_int_env("MAX_SHARE_LINK_MAX_DOWNLOADS", 25)
    LOGIN_RATE_LIMIT_ATTEMPTS = read_int_env("LOGIN_RATE_LIMIT_ATTEMPTS", 8)
    LOGIN_RATE_LIMIT_WINDOW_SECONDS = read_int_env(
        "LOGIN_RATE_LIMIT_WINDOW_SECONDS", 5 * 60
    )
    UPLOAD_RATE_LIMIT_REQUESTS = read_int_env("UPLOAD_RATE_LIMIT_REQUESTS", 20)
    UPLOAD_RATE_LIMIT_WINDOW_SECONDS = read_int_env(
        "UPLOAD_RATE_LIMIT_WINDOW_SECONDS", 15 * 60
    )
    STORAGE_ENCRYPTION_MODE = os.getenv("STORAGE_ENCRYPTION_MODE", "server-side")
    KEY_MANAGEMENT_STRATEGY = os.getenv(
        "KEY_MANAGEMENT_STRATEGY", "platform-managed"
    )
    CORS_ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ALLOWED_ORIGINS",
            "http://localhost:8080,http://127.0.0.1:8080,http://localhost:8081,http://127.0.0.1:8081",
        ).split(",")
        if origin.strip()
    ]
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    API_PREFIX = "/api/v1"
    AUTO_INIT_DB = os.getenv("AUTO_INIT_DB", "true").lower() == "true"
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
