from collections import defaultdict, deque
from functools import wraps
from threading import Lock
from time import monotonic

from flask import current_app, request

from ..utils.responses import error_response


class InMemoryRateLimiter:
    def __init__(self):
        self._entries = defaultdict(deque)
        self._lock = Lock()

    def allow_request(self, key, limit, window_seconds):
        now = monotonic()

        with self._lock:
            bucket = self._entries[key]
            boundary = now - window_seconds

            while bucket and bucket[0] <= boundary:
                bucket.popleft()

            if len(bucket) >= limit:
                retry_after = max(1, int(window_seconds - (now - bucket[0])))
                return False, retry_after

            bucket.append(now)
            return True, None

    def reset(self):
        with self._lock:
            self._entries.clear()


rate_limiter = InMemoryRateLimiter()


def rate_limit(*, limit_config_key, window_config_key, key_func, message):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped(*args, **kwargs):
            limit = current_app.config[limit_config_key]
            window_seconds = current_app.config[window_config_key]
            allowed, retry_after = rate_limiter.allow_request(
                key=key_func(),
                limit=limit,
                window_seconds=window_seconds,
            )

            if not allowed:
                return error_response(
                    message=message,
                    status=429,
                    headers={"Retry-After": str(retry_after)},
                )

            return view_function(*args, **kwargs)

        return wrapped

    return decorator


def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"
