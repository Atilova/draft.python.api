from src.infra.config import load_config


_config = load_config()

bind = _config.gunicorn.bind
workers = _config.gunicorn.workers
threads = _config.gunicorn.threads
worker_class = _config.gunicorn.worker_class
loglevel = _config.gunicorn.loglevel
timeout = _config.gunicorn.timeout

if _config.gunicorn.access_logs:
    accesslog = "-"
