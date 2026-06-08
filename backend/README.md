# Backend

FastAPI backend for Library Management System.

## Technologies

- FastAPI
- MongoDB
- JWT Authentication
- Bcrypt

## Folder Structure

backend/
├── routes/
├── services/
├── schema/
├── core/

## Environment Variables

Create a .env file:

JWT_SECRET_KEY=your_secret_key
MONGODB_URL=your_connection_string

## Installation

pip install -r requirements.txt

## Run

python -m backend.main

## API Documentation

http://localhost:8080/docs

## Main Endpoints

### Authentication

POST /auth/signup
POST /auth/login

### Books

GET /books
POST /books
PUT /books/{id}
DELETE /books/{id}

### Issues

POST /issue
PUT /issue/{id}/return
GET /issue/me

### Users

GET /users
DELETE /users/{id}
PUT /users/{id}/role