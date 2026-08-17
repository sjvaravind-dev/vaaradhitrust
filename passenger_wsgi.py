"""
Hostinger / LiteSpeed Passenger entry point.

hPanel → Advanced → Python:
  Application URL:   https://vaaradhi.gayatritechsolutions.com
  Application root:  this directory (manage.py lives here)
  Startup file:      passenger_wsgi.py
  Application entry: application

Never open this file as a website URL.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(BASE_DIR, ".env"))
except Exception:
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
