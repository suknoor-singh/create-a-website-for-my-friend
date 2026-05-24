# AWS Lightsail deployment

This is the recommended low-cost production path for Ajmani and Law Partners.

## Target setup

- 1 Ubuntu Lightsail instance
- 1 static IP
- GoDaddy domain pointing to the Lightsail IP
- Django + Wagtail running with `gunicorn`
- `nginx` as reverse proxy
- SQLite kept on the server filesystem for launch

For your current account, the created resources are:

- Instance: `ajmani-web-01-ubuntu`
- Static IP: `13.207.66.255`
- Database: `ajmani-db-01`
- Bucket: `ajmani-media-prod`

## Server packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git
```

## App setup

```bash
cd /var/www
sudo mkdir -p /var/www/ajmaniandlawpartners
sudo chown $USER:$USER /var/www/ajmaniandlawpartners
cd /var/www/ajmaniandlawpartners

git clone <YOUR_REPO_URL> app
cd app/ajmani_site

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

## Environment file

Create `.env.production` beside `manage.py` using `.env.production.example` as the base.

Important values:

- `DJANGO_SETTINGS_MODULE=ajmani_site.settings.production`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `WAGTAILADMIN_BASE_URL`
- `DB_*`
- `USE_S3_MEDIA=true`
- `AWS_STORAGE_BUCKET_NAME`

Load it before management commands:

```bash
set -a
source .env.production
set +a
```

## Django commands

```bash
python manage.py migrate
python manage.py seed_ajmani_content
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Lightsail bucket permissions

Before uploads can work correctly, go to the Lightsail bucket:

1. Open `ajmani-media-prod`
2. Go to `Permissions`
3. Set bucket access to `All objects are public (read-only)` for the first launch
4. In `Resource access`, attach the instance `ajmani-web-01-ubuntu`

AWS says attaching the instance gives it full programmatic access to the bucket without manually managing credentials.

## Gunicorn service

Create `/etc/systemd/system/ajmani.service`:

```ini
[Unit]
Description=Ajmani and Law Partners gunicorn
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/ajmaniandlawpartners/app/ajmani_site
EnvironmentFile=/var/www/ajmaniandlawpartners/app/ajmani_site/.env.production
ExecStart=/var/www/ajmaniandlawpartners/app/ajmani_site/.venv/bin/gunicorn ajmani_site.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ajmani
sudo systemctl start ajmani
sudo systemctl status ajmani
```

## Nginx site

Create `/etc/nginx/sites-available/ajmaniandlawpartners`:

```nginx
server {
    listen 80;
    server_name 13.207.66.255;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/ajmaniandlawpartners/app/static/;
    }

    location /media/ {
        alias /var/www/ajmaniandlawpartners/app/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/ajmaniandlawpartners /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL

After DNS is pointing correctly:

```bash
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx -d ajmaniandlawpartners.com -d www.ajmaniandlawpartners.com
```

## GoDaddy DNS

Create `A` records for:

- `@` -> Lightsail static IP
- `www` -> Lightsail static IP

## Uploading newsletters

After deployment, use `/admin/`:

1. Open `Newsletters`
2. Add a `Newsletter Page`
3. Upload the PDF in `PDF document`
4. Publish

## Current launch sequence

Since the domain is not being attached yet:

1. Launch the site on `http://13.207.66.255/`
2. Verify homepage, admin, uploads, and database-backed pages
3. Later point GoDaddy to the same static IP
4. Then switch `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `WAGTAILADMIN_BASE_URL`
5. Then enable SSL and set `SECURE_SSL_REDIRECT=true`
