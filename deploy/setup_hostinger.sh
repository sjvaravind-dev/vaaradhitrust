#!/bin/bash
set -e
pip install -r requirements.txt
python manage.py setup_hosting
echo "Done. Open the Application URL and restart the Python app in hPanel."
