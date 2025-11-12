# Gunicorn configuration file
import os
import multiprocessing

# Server socket
bind = "0.0.0.0:8080"
backlog = 2048

# Worker processes
# For I/O-bound applications, 2-4x CPU cores is typical
workers = max(2, multiprocessing.cpu_count() * 2)
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes - increased for large file transfers
keepalive = 75

# Process naming
proc_name = "TemplateService"

# Logging
loglevel = "info"
accesslog = "-"  # stdout
errorlog = "-"   # stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None
ca_certs = None
cert_reqs = 0
do_handshake_on_connect = False
ssl_version = 2

# Reloading
reload = False

# Server hooks


def pre_fork(server, worker):
    pass


def post_fork(server, worker):
    pass


def pre_exec(server):
    pass


def when_ready(server):
    print("Gunicorn server is ready. Spawning workers")


def pre_request(worker, req):
    worker.log.debug('%s %s' % (req.method, req.path))


def post_request(worker, req, environ, resp):
    pass


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
