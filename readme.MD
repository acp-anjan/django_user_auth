
# Django User Auth Project

This project contains a app for django for user authentication. 



## Tech Stack

**Server:** Sqlite, Django

**Frontend:** Html, Bootstrap

**Initial Setup**: Installation of python in developer's system



## Run Locally

Clone the project

```bash
  git clone https://github.com/acp-anjan/django_user_auth.git
```

For the first time, create virtual environment and activate it.

```bash
  python -m venv venv
```
Before working on project activate it before
```bash
  venv/Script/activate
```

Go to the project directory

```bash
  cd custom_auth
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Mirgrate to db:

Currently, SQLite is setup. However, it can be changed before this from settings.py

For SMTP email use, change email settings in settings.py.

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

