# Secure File Transfer System

## Description

This project is a secure file transfer system that allows users to upload and download files securely using SSL/TLS encryption. The system is built using Flask (Python) for the backend and supports user authentication with JWT tokens.

## Features

- User registration and login
- Secure file upload
- Secure file download
- SSL/TLS encryption for secure communication

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: SSL/TLS encryption using OpenSSL
- **Development Tools**: Python, Docker, Git
- **Testing Tools**: Curl

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- Virtualenv
- OpenSSL
- Git
- Docker (optional, for containerization)

### Step-by-Step Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/vikramsinghbrahm/secure-file-transfer.git
cd secure-file-transfer
```

#### 2. Set Up the Virtual Environment
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
#### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```
#### 4. Generate SSL Certificates
Navigate to the backend/certs directory and generate SSL certificates:
```bash
mkdir backend/certs
cd backend/certs
openssl genpkey -algorithm RSA -out key.pem
openssl req -new -key key.pem -out csr.pem
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem
cd ../..
```

#### 5. Run the Application
Navigate to the backend directory and start the Flask application:
```bash
cd backend
python run.py
```
## Usage
#### Register a New User
```bash
curl -X POST https://localhost:5000/register -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"testpassword\"}" --insecure
```
#### Log In
```bash
curl -X POST https://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"testpassword\"}" --insecure
```
Save the JWT token from the response.
#### Upload a File
Replace <TOKEN> with the JWT token you received from the login command, and replace path\to\your\file.txt with the actual path to the file you want to upload:
```bash
curl -X POST https://localhost:5000/upload -H "Authorization: Bearer <TOKEN>" -F "file=@path\to\your\file.txt" --insecure
```
#### Download a File
Replace <TOKEN> with the JWT token you received from the login command, and replace filename.txt with the actual name of the file you uploaded:
```bash
curl -X GET https://localhost:5000/download/filename.txt -H "Authorization: Bearer <TOKEN>" --insecure -o downloaded_file.txt
```
## Docker Support
To run the application using Docker, follow these steps:

#### 1. Build the Docker Image
```bash
docker build -t secure-file-transfer-backend ./backend
```
#### 2. Run the Docker Container
```bash
docker run -d -p 5000:5000 --name secure-file-transfer-backend secure-file-transfer-backend
```
##### Contributing
Contributions are welcome! Please create an issue or submit a pull request.
