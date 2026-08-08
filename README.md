# Property Finds — Backend (Django)

Self-contained Django API + admin for Property Finds.

## Run locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser   # optional
python manage.py runserver 0.0.0.0:8000
```

## Layout

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── media/                 # uploaded images
└── backend/               # project package
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── asgi.py
    ├── app/               # listings models, API, admin
    ├── templates/
    └── static/
```

## Production notes

- Set `CORS_ALLOW_ALL_ORIGINS=false` and `CORS_ALLOWED_ORIGINS` to your frontend URL
- Serve `media/` files (or move to S3/Cloudinary)
- Prefer Postgres instead of SQLite for production
