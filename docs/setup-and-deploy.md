# Setup and deploy guide

## Install locally

1. Install `Python 3.11+`.
2. Create a virtual environment in the workspace root.
3. Install Wagtail.
4. Run Django migrations.
5. Create a superuser.
6. Start the development server.

Commands:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\ajmani_site\requirements.txt
cd .\ajmani_site\
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py seed_ajmani_content
..\.venv\Scripts\python.exe manage.py createsuperuser
..\.venv\Scripts\python.exe manage.py runserver
```

## Production setup on AWS Lightsail

1. Create a small Ubuntu Lightsail instance.
2. Attach a static IP.
3. Install `python3`, `python3-venv`, `nginx`, and `git`.
4. Clone the project.
5. Create a Linux virtual environment and install requirements.
6. Run `manage.py migrate` and `manage.py collectstatic`.
7. Run the app behind `gunicorn`.
8. Reverse proxy with `nginx`.
9. Point your GoDaddy domain `A` record to the Lightsail static IP.
10. Add `https` with `certbot` and LetsEncrypt.

## Why not Angular first

Angular is absolutely workable, but for this project it adds build complexity, more deployment moving parts, and no real benefit unless you want a highly interactive client portal or dashboard later.

## When to upgrade from SQLite

Keep SQLite for launch if:

- traffic is low to moderate
- there is one small admin team
- you are running one server

Move to PostgreSQL later if:

- traffic becomes heavy
- you add more editors
- you add more complex form submissions or integrations
