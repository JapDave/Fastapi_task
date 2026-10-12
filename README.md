# FastAPI authentication and posts API

A compact backend exercise demonstrating request validation, database sessions, password hashing, bearer authentication and ownership-scoped CRUD. Built with FastAPI, SQLAlchemy and SQLite.

## Run locally

Use Python 3.12. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API. The local SQLite schema is created at startup. Set `DATABASE_URL` to override the database connection.

## API flow

1. `POST /auth/signup` with `email` and `password` (8–128 characters) returns a token.
2. Send `Authorization: Bearer <token>` to protected routes. The original `token` header is also supported.
3. `POST /posts` with `{"text": "Hello"}` creates a post and returns its numeric `postID`.
4. `GET /posts` lists your posts; `DELETE /posts/{postID}` deletes only your own post.
5. `POST /auth/login` validates the password and rotates the user's token.

Passwords use salted scrypt hashes. List reads query the database directly to avoid stale process-local caches. Existing demo databases with plaintext passwords should be recreated; no automatic migration of legacy passwords is performed.

## Verification

```bash
python -m pytest -q
```

Tests cover password storage, duplicate signup, failed login, token rotation, protected routes, post ownership and fresh reads after writes. Tests use an isolated in-memory database.

## Scope

This is a learning/reference API, not a complete production identity system. Tokens are stored in the database and have no expiry; token revocation, rate limiting, deployment configuration and schema migrations are future work. Use HTTPS and a suitable identity design before exposing it publicly.

A GitHub Actions test template is provided in `docs/ci/tests.yml`. To enable it, copy it to `.github/workflows/tests.yml`.
