


# gunicorn_config.py
bind = "0.0.0.0:8000"  # Address and port to bind
workers = 3  # Number of worker processes
timeout = 120  # Timeout for workers
accesslog = "-"  # Access log (use "-" for stdout)
errorlog = "-"  # Error log (use "-" for stderr)