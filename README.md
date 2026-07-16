# Arash's Blog

A Flask blog application with authentication, admin-managed posts, rich-text
comments, and a SQLite development database.

## Features

- User registration, login, and logout
- Admin-only post creation, editing, and deletion
- Quill-powered rich-text posts and comments with server-side HTML sanitization
- CSRF-protected forms and POST-only state-changing actions
- Environment-based secrets and deployment configuration
- Automated route, authorization, CRUD, and sanitization tests

## Local setup

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Replace `SECRET_KEY` in `.env` with a random value. One way to generate it is:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Run the application:

```powershell
flask --app main run --debug
```

Add or refresh the three demo articles after creating the admin account:

```powershell
flask --app main seed-content
```

The command preserves unrelated posts, accounts, and comments. It can be run
again whenever the bundled starter articles are updated.

The database is created automatically in `instance/blog.db`. The first user
normally receives ID `1`; set `ADMIN_USER_ID` in `.env` to the ID that should
manage posts.

## Tests

```powershell
pytest
```

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Session and CSRF signing key | Required |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///blog.db` |
| `ADMIN_USER_ID` | User ID allowed to manage posts | `1` |
| `CONTACT_EMAIL` | Optional public contact address | Empty |
| `FLASK_DEBUG` | Enables debug mode only when set to `1` | Disabled |

Never commit `.env` or a database containing real user data. Use
`.env.example` to document configuration safely.
