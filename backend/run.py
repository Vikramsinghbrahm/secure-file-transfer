import os
import ssl

from app import create_app

app = create_app()


def build_ssl_context():
    cert_path = os.getenv("TLS_CERT_PATH")
    key_path = os.getenv("TLS_KEY_PATH")

    if not cert_path or not key_path:
        return None

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_path, key_path)
    return context


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5001")),
        ssl_context=build_ssl_context(),
    )
