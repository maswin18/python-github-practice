## Project Demo (Local API)
- Base URL: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs

# Inventory API (FastAPI + JWT Auth)

## Overview
This is a backend API built using FastAPI with full CRUD functionality, database integration, and authentication.

## Features
- Create, Read, Update, Delete (CRUD) for products
- SQLite database using SQLAlchemy
- User registration and login
- JWT authentication (secure endpoints)
- Password hashing using bcrypy
- Environment variable for SECRET_KEY

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)

## How to Run

### 1. Install dependencies
pip install fastapi uvicorn sqlalchemy python-jose passlib[bcrypt]

### 2. Set environment variable (Windows)
setx SECRET_KEY "your_secret_key"

### 3. Run server
uvicorn app:app --reload

## API Endpoints

### Auth
- POST /register
- POST /login

### Products (Protected)
- GET /products
- POST /products
- PUT /products/{id}
- DELETE /products/{id}

## Notes
- Protected endpoints require Authorization header:
  Bearer <access_token>