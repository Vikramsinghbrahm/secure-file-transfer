import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

_fernet_cache: dict[int, Fernet] = {}

_KDF_SALT = b"vaultflow-storage-v1"
_KDF_ITERATIONS = 100_000


def get_fernet(app) -> Fernet | None:
    """Return a Fernet cipher for the app, or None if encryption is disabled."""
    if app.config.get("STORAGE_ENCRYPTION_MODE") != "server-side":
        return None

    app_id = id(app)
    if app_id not in _fernet_cache:
        _fernet_cache[app_id] = Fernet(_resolve_key(app))
    return _fernet_cache[app_id]


def _resolve_key(app) -> bytes:
    explicit_key = (app.config.get("STORAGE_ENCRYPTION_KEY") or "").strip()
    if explicit_key:
        return explicit_key.encode()

    secret = app.config["SECRET_KEY"].encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_KDF_SALT,
        iterations=_KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(secret))
