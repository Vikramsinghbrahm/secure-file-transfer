from app import app, db
import ssl

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certs/cert.pem', 'certs/key.pem')

    app.run(ssl_context=context, host='0.0.0.0', port=5000)
