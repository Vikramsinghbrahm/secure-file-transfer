import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '5001')}"

# 2-4 workers is right for a CPU-bound Flask app behind a proxy.
# For a file-transfer workload (I/O-bound), go higher.
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"

# Recycle workers periodically to prevent memory creep.
max_requests = 1000
max_requests_jitter = 100

# How long a worker has to finish its in-flight request on SIGTERM before
# the master kills it. Long enough for a 25 MB upload at modest bandwidth.
graceful_timeout = 30
timeout = 120

keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"

# Forward the original client IP from a reverse proxy.
forwarded_allow_ips = "*"
