# Vaaradhi Trust Website

Professional, responsive NGO website inspired by [Nirmaan](https://nirmaan.org/), rebuilt with **Django + Django REST Framework + HTML/CSS/JS**. Content from [vaaradhi.org.in](https://vaaradhi.org.in/) is seeded and editable via admin / API.

## Stack

- Django 6 + DRF (JSON API under `/api/v1/`)
- Server-rendered templates for SEO
- Whitenoise compressed static files
- Page caching + API caching
- Optional Redis cache
- Traffic hit buffering middleware
- Sitemap + robots.txt + JSON-LD + Open Graph

## Quick start (Windows / XAMPP folder)

```powershell
cd c:\xampp8\htdocs\vaaradhi
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_content
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Site: http://127.0.0.1:8000/
- Admin CMS: http://127.0.0.1:8000/admin/
- API home bundle: http://127.0.0.1:8000/api/v1/home/

## Dynamic vs static (CMS)

| Area | Mode | Admin model |
|------|------|-------------|
| Main slider | Dynamic | Home Slider |
| Our Impact | Dynamic | Impact Stats |
| Initiatives for Change | Dynamic | Initiatives |
| Events (nav → LinkedIn) | Dynamic + redirect | Events + Site Settings `events_linkedin_url` |
| Partners / logos | Dynamic | Partners |
| Testimonials | Dynamic | Testimonials |
| Media & News | Dynamic | Media & News |
| Active / Ongoing projects | Dynamic | Projects |
| Careers / campaigns | Dynamic | Careers, Donation Campaigns |
| Scrolling news + popup image | Dynamic | Scrolling News, Popup Banner |
| Who we are / Vision / Mission / Story / Privacy / Volunteer / CSR / Footer | Static / semi-static | Site Settings |
| Team / Governance docs | Semi-static | Team Members, Governance Documents |

## Navigation map

- **About Us:** Our Story, Vision & Mission, Team, Governance, Privacy Policy, Media & News
- **Programs:** Urban Forestry, Skill Development, Generic Medicines, Education, Legal Awareness, Plastic Waste, FPOs, etc.
- **Our Work:** Active Projects, Ongoing Projects
- **Events:** redirects to Vaaradhi LinkedIn
- **Partners**
- **Join Us:** Careers, Volunteer, CSR Partnership
- **Donate Now** CTA

## Production notes (traffic)

1. Set `DJANGO_DEBUG=False`, strong `DJANGO_SECRET_KEY`, and real `ALLOWED_HOSTS`.
2. Use PostgreSQL/MySQL + `REDIS_URL` for cache.
3. Collect static: `python manage.py collectstatic`
4. Run behind Nginx/Apache with Gunicorn workers:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2 --timeout 60
```

5. Recommended reverse-proxy cache for anonymous HTML (`Cache-Control` already helped by `cache_page`).

## Hosting / 403 Forbidden

Apache/LiteSpeed returns **403 Forbidden** if this folder is opened as a normal website. Django has no `index.html`; it must run as a Python WSGI app.

### Option A — cPanel / LiteSpeed (Passenger)

1. Create a **Python App** in cPanel.
2. App root = this project folder.
3. Startup file = `passenger_wsgi.py`
4. Create a virtualenv, then:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_content
```

5. In `.env` set your live domain (and IP if you open the site by IP):

```
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=vaaradhi.org.in,www.vaaradhi.org.in,YOUR_SERVER_IP
SITE_URL=https://vaaradhi.org.in
```

Set the domain document root to the `public` folder if cPanel asks for one.

### Option B — XAMPP on this PC

Do **not** open `http://localhost/vaaradhi/` in Apache. That folder is not a static site.

1. Double-click `start-host.bat` (Django on port 8000).
2. Optional: add `deploy/xampp-vhost.conf` to Apache and proxy `/` to `http://127.0.0.1:8000/`.
3. Or just use `http://127.0.0.1:8000/`.

## SEO included

- Unique title/description per major page
- Canonical URLs
- Open Graph / Twitter cards
- Organization JSON-LD
- `/sitemap.xml` and `/robots.txt`

## License / ownership

Built for Vaaradhi Trust internal use.
