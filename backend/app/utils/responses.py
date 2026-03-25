from flask import g, jsonify


def success_response(*, data=None, message="OK", status=200):
    payload = {
        "message": message,
        "requestId": getattr(g, "request_id", None),
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status


def error_response(*, message, status, headers=None):
    response = jsonify(
        {
            "message": message,
            "requestId": getattr(g, "request_id", None),
        }
    )
    if headers:
        response.headers.update(headers)
    return response, status
