# FastAPI Blogging App

This is a simple blogging app built using FastAPI, SQLAlchemy, and caching.

## Project Structure

FASTAPI_TASK/
├── app/
│ ├── init.py # Main FastAPI application entry point
│ ├── database.py # Database initialization and functions
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── auth.py # Authentication endpoints
│ |── posts.py # Post-related endpoints
│ │── cache.py # Caching implementation


## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/JapDave/Fastapi_task.git
cd Fastapi_task

pip install -r requirements.txt
uvicorn app:app --reload
