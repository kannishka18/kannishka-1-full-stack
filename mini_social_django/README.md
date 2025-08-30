# Mini Social (Django)

A polished mini social media app built with Django.

## Features
- Sign up, login, logout (Django auth)
- User profiles with avatar + bio
- Create posts with optional image
- Comments
- Like/unlike posts (AJAX)
- Follow/unfollow users (AJAX)
- Feed shows your posts + people you follow
- Bootstrap 5 UI

## Quickstart

```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Start project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

## Notes
- Uploaded media are stored in `media/` (dev only). 
- For production, set `DEBUG=False`, add `ALLOWED_HOSTS`, and configure static/media hosting (e.g., WhiteNoise + S3).
