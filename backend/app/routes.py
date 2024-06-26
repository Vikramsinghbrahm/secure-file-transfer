import os
import logging
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from app.models import User, File, Log
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'User already exists'}), 400
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully'}), 201
    except Exception as e:
        app.logger.error(f"Error in /register: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Login failed'}), 401
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    except Exception as e:
        app.logger.error(f"Error in /login: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        current_user_id = get_jwt_identity()
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        new_file = File(filename=filename, user_id=current_user_id)
        db.session.add(new_file)
        db.session.commit()
        return 'File uploaded', 201
    except Exception as e:
        app.logger.error(f"Error in /upload: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download_file(filename):
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        app.logger.debug(f"Files in upload directory: {files}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        app.logger.error(f"Error in /download/{filename}: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
