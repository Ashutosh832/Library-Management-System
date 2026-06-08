# Library Management System

## Overview

A full-stack Library Management System built using React, FastAPI, and MongoDB.

The application supports role-based access control with separate Admin and Student dashboards. Students can browse books, issue books, return books, and view their issue history. Admins can manage books, users, and monitor all issue records.

---

## Features

### Authentication

* User Signup
* User Login
* JWT Authentication
* Role-Based Access Control (Admin / Student)

### Student Features

* View all books
* Search books
* Issue books
* Return books
* View issued books
* Logout

### Admin Features

* View active issues
* View issue logs/history
* View all users
* Update user roles
* Delete users
* View all books
* Create books
* Update books
* Delete books
* Logout

---

## Tech Stack

### Frontend

* React
* React Router
* Fetch API
* CSS

### Backend

* FastAPI
* Pydantic
* JWT Authentication
* BCrypt Password Hashing

### Database

* MongoDB

---

## Project Structure

```text
Library Management/
│
├── backend/
│   ├── routes/
│   ├── services/
│   ├── schema/
│   ├── core/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── util/
│   │   └── App.js
│
└── README.md
```

---

## Authentication Flow

1. User logs in using email and password.
2. Backend validates credentials.
3. JWT access token is generated.
4. Token is stored in Local Storage.
5. Frontend sends token in Authorization header.
6. Protected endpoints validate the token.
7. User permissions are determined by role.

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Library-Management-System
```

### Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
JWT_SECRET_KEY=your_secret_key
MONGODB_URL=your_mongodb_connection_string
```

Run Backend:

```bash
python -m backend.main
```

Backend URL:

```text
http://localhost:8080
```

Swagger Documentation:

```text
http://localhost:8080/docs
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend URL:

```text
http://localhost:3000
```

---

## API Overview

### Authentication

```text
POST /auth/signup
POST /auth/login
```

### Books

```text
GET    /books
POST   /books
PUT    /books/{book_id}
DELETE /books/{book_id}
GET    /books/search
```

### Issues

```text
POST   /issue
PUT    /issue/{issue_id}/return
GET    /issue
GET    /issue/me
GET    /issue/active
```

### Users

```text
GET    /users
DELETE /users/{user_id}
PUT    /users/{user_id}/role
```

---

## Future Improvements

* Protected frontend routes
* Pagination
* Docker deployment
* Unit testing
* Refresh tokens
* Book availability tracking
* Email notifications

---

## Author

Ashutosh Nayak

Final Year Computer Science Engineering Student
