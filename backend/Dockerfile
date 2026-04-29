FROM python:3.12-slim

WORKDIR /app

COPY requirements.prod.txt ./
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .

EXPOSE 5001

# Run schema migrations then hand off to gunicorn.
# Gunicorn handles SIGTERM gracefully (graceful_timeout=30 in gunicorn.conf.py).
CMD ["sh", "-c", "python -m flask --app run.py db upgrade && gunicorn --config gunicorn.conf.py 'run:app'"]
