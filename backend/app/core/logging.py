import json
import logging
import traceback
from datetime import UTC, datetime


class _RequestContextFilter(logging.Filter):
    def filter(self, record):
        try:
            from flask import g, has_request_context, request

            if has_request_context():
                record.request_id = getattr(g, "request_id", "-")
                record.method = request.method
                record.path = request.path
            else:
                record.request_id = "-"
                record.method = "-"
                record.path = "-"
        except Exception:
            record.request_id = "-"
            record.method = "-"
            record.path = "-"
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }

        method = getattr(record, "method", "-")
        path = getattr(record, "path", "-")
        if method != "-":
            payload["method"] = method
            payload["path"] = path

        if record.exc_info:
            payload["exc"] = traceback.format_exception(*record.exc_info)

        return json.dumps(payload)


def configure_json_logging(app):
    if app.logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(_RequestContextFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.propagate = True

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
