# 🚀 Smart Queue Management System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-green?style=for-the-badge)

</p>

<p align="center">

A <b>Full Stack Queue Management System</b> built using <b>FastAPI</b>, <b>PostgreSQL</b>, and <b>Streamlit</b> that streamlines queue operations for hospitals, banks, colleges, government offices, and service centers through secure authentication, automated token generation, and real-time queue management.

</p>

---

# 📖 Overview

The **Smart Queue Management System** is a full-stack application designed to digitize and automate queue management processes. Traditional queue systems often rely on manual token distribution, resulting in long waiting times, inefficient customer handling, and poor service management.

This application replaces conventional methods with a centralized digital platform where users can securely authenticate, join service queues, receive automatically generated tokens, and track their queue status while administrators efficiently manage customer flow through an intuitive dashboard.

The system follows modern backend development practices using **FastAPI**, **REST APIs**, **JWT Authentication**, **SQLAlchemy ORM**, and **PostgreSQL**, with a **Streamlit frontend** providing an interactive interface.

---

# 🎯 Problem Statement

Many organizations continue to use manual queue management methods which often result in:

- Long waiting times
- Poor customer experience
- Manual token distribution
- Lack of transparency
- Difficulty handling priority customers
- Inefficient service allocation
- No centralized queue monitoring
- Time-consuming administrative tasks

These challenges reduce operational efficiency and negatively affect customer satisfaction.

---

# 💡 Solution

The Smart Queue Management System automates the complete queue lifecycle by providing:

- Secure user authentication
- Digital token generation
- Queue creation and management
- FIFO queue processing
- Priority queue handling
- Queue analytics
- REST APIs
- Interactive dashboard

The system improves customer experience while enabling administrators to manage queues more efficiently.

---

# ✨ Key Features

## 🔐 Authentication & Security

- User Registration
- Secure Login
- JWT Authentication
- Password Hashing
- Protected API Routes
- Role-Based Access Control

---

## 👤 User Features

- Register Account
- Login Securely
- Join Available Queues
- Receive Digital Queue Token
- Track Queue Status
- View Queue Details

---

## 👨‍💼 Administrator Features

- Create New Queues
- Manage Existing Queues
- Call Next Customer
- Update Token Status
- Monitor Active Queues
- View Analytics Dashboard

---

## 🎟 Token Management

- Automatic Token Generation
- Sequential Tokens (A001, A002...)
- FIFO Queue Processing
- Priority Queue Support
- Token Status Updates
- Queue Position Tracking

---

## 📊 Dashboard & Analytics

- Total Users
- Total Queues
- Total Tokens
- Active Customers
- Completed Services
- Queue Statistics

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Programming Language | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Hashing | Passlib |
| Validation | Pydantic |
| API Documentation | Swagger UI |
| Server | Uvicorn |

---

# 🏗 Full Stack Architecture

```
                 User
                  │
                  ▼
         Streamlit Frontend
                  │
                  ▼
         FastAPI REST APIs
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
 Authentication Queue Logic Analytics
        │         │         │
        └─────────┼─────────┘
                  ▼
          SQLAlchemy ORM
                  │
                  ▼
          PostgreSQL Database
```

---

# ⚙️ Workflow

```
User Registration
        │
        ▼
Login Authentication
        │
        ▼
JWT Token Generated
        │
        ▼
Join Queue
        │
        ▼
Generate Queue Token
        │
        ▼
Waiting Queue
        │
        ▼
Administrator Calls Next Customer
        │
        ▼
Service Completed
```

---

# 📂 Project Structure

```
Smart-Queue-Management-System
│
├── app
│   ├── app.py
│   ├── database.py
│   ├── create_tables.py
│   ├── schemas.py
│   ├── utils.py
│   │
│   ├── models
│   │   ├── user.py
│   │   ├── queue.py
│   │   └── token.py
│   │
│   ├── services
│   │   └── token_service.py
│   │
│   └── frontend
│       ├── Home.py
│       └── pages
│
├── requirements.txt
├── README.md
└── .env
```

---

# 🗄 Database Design

The application uses a relational PostgreSQL database.

### User

Stores registered user information.

**Fields**

- User ID
- Name
- Email
- Password
- Role

---

### Queue

Stores queue information.

**Fields**

- Queue ID
- Queue Name
- Description
- Created Time

---

### Token

Stores generated queue tokens.

**Fields**

- Token Number
- Status
- Queue ID
- User ID
- Priority
- Created Time

---

## Database Relationships

```
User
 │
 │ 1
 │
 │ N
 ▼
Token
 ▲
 │ N
 │
 │ 1
Queue
```

---

# 🧠 Data Structures & Algorithms

This project implements multiple data structures and algorithms to efficiently manage queues.

### FIFO Queue

Customers are served in the exact order they join.

### Priority Queue

Priority customers (VIP/Emergency) are served before regular customers.

### Sequential Token Generation

Automatically generates unique queue numbers.

Example:

```
A001
A002
A003
A004
```

### Sorting

Customers are sorted based on:

- Priority
- Queue Entry Time

---

# 🔗 REST API Endpoints

## Authentication APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /signup | Register User |
| POST | /login | Login User |
| GET | /users | Get All Users |

---

## Queue APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /queues | Create Queue |
| GET | /queues | View Queues |
| GET | /queues/{id} | Queue Details |

---

## Token APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /queues/{id}/join | Join Queue |
| GET | /queues/{id}/tokens | View Tokens |
| POST | /queues/{id}/call-next | Call Next Customer |
| PUT | /tokens/{id}/status | Update Token Status |

---

## Dashboard APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /analytics/dashboard | Queue Analytics |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/mansiym13-sketch/Smart-Queue-Management-System-v2.git
```

Move into the project directory

```bash
cd Smart-Queue-Management-System-v2
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Backend

```bash
uvicorn app.app:app --reload
```

Backend will run at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# 🖥 Running the Frontend

Run the Streamlit application

```bash
streamlit run app/frontend/Home.py
```

---

# 📦 Sample API Response

```json
{
    "token_number": "A005",
    "queue_id": 1,
    "status": "Waiting",
    "priority": "Normal"
}
```

---


# 🚀 Future Enhancements

- Docker Containerization
- Kubernetes Deployment
- Redis Queue Caching
- WebSocket Live Queue Updates
- SMS Notifications
- Email Notifications
- QR Code Tokens
- AI Waiting Time Prediction
- Mobile Application
- Multi-Branch Queue Management
- Appointment Scheduling
- Cloud Deployment (AWS)

---

# ⚡ Challenges Faced

During development, I encountered several technical challenges:

- Designing scalable queue management logic
- Implementing secure JWT Authentication
- Maintaining proper database relationships
- Sequential token generation
- Supporting FIFO and Priority Queue processing
- Creating reusable REST APIs
- Structuring the project using modular architecture
- Integrating frontend with backend services

---

# 📚 What I Learned

This project significantly strengthened my understanding of:

- Full Stack Application Development
- FastAPI Framework
- REST API Development
- PostgreSQL Database Design
- SQLAlchemy ORM
- JWT Authentication
- Password Hashing
- Pydantic Validation
- CRUD Operations
- Queue Data Structures
- API Documentation using Swagger
- Backend Architecture
- Frontend & Backend Integration
- Clean Code Practices

---

# 🎯 Real-World Applications

This solution can be adopted by:

- 🏥 Hospitals
- 🏦 Banks
- 🏢 Government Offices
- 🎓 Colleges & Universities
- 🏪 Retail Stores
- 🩺 Clinics
- 📮 Passport Offices
- 💼 Corporate Offices
- 🏢 Customer Service Centers

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve the project:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request


# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.

It motivates me to continue building impactful projects and sharing them with the developer community.
