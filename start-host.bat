@echo off
cd /d "%~dp0"
echo Starting Vaaradhi Trust Django on http://127.0.0.1:8000
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python -m gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3 --threads 2 --timeout 60
pause
