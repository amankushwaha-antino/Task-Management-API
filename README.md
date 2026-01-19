# Task Management API

Lightweight Flask-based task management API for demonstration and local development.

## Features
- User registration, login, logout (access + refresh token revoke)
- JWT authentication (access + refresh tokens)
- Create, read, update, delete tasks
- Task stats and filtering

## Quick start

1. Create and activate a virtual environment (Windows):

```powershell
python -m venv venv
venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the server:

```powershell
python server.py
```

The API will be available at `http://127.0.0.1:5000`.

## Important endpoints

- `POST /api/v1/auth/register` — register user
- `POST /api/v1/auth/login` — obtain access and refresh tokens
- `POST /api/v1/auth/logout` — revoke access token
- `POST /api/v1/auth/logout/refresh` — revoke refresh token
- `POST /api/v1/auth/refresh` — exchange refresh for new access token
- `GET /api/v1/auth/me` — get current user

- `POST /api/v1/tasks` — create task
- `GET /api/v1/tasks` — list tasks
- `GET /api/v1/tasks/<id>` — get single task
- `PUT /api/v1/tasks/<id>` — update task
- `DELETE /api/v1/tasks/<id>` — delete task
- `GET /api/v1/tasks/stats` — task statistics

## Notes
- Use the `Authorization: Bearer <ACCESS_TOKEN>` header for protected routes.
- Avoid trailing slashes when calling `/api/v1/tasks` endpoints (server routes configured without trailing slash).


