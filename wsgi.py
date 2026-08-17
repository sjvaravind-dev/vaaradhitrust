"""Hosting panels that look for wsgi.py instead of passenger_wsgi.py."""
from passenger_wsgi import application  # noqa: F401
