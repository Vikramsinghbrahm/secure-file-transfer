from flask import current_app
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge

from ..utils.responses import error_response


class ApiError(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return error_response(message=error.message, status=error.status_code)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_request(_error):
        max_size_mb = app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)
        return error_response(
            message=f"File exceeds the {max_size_mb} MB upload limit.",
            status=413,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return error_response(message=error.description, status=error.code)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        current_app.logger.exception("Unhandled application error: %s", error)
        return error_response(message="Internal server error.", status=500)
