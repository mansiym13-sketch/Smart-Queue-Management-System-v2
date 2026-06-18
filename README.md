# Smart Queue Management System

## Overview

The Smart Queue Management System is a backend application developed using FastAPI and PostgreSQL to automate and optimize customer queue handling in service environments such as banks, hospitals, government offices, and customer service centers.

The system enables users to register, authenticate securely using JWT tokens, join service queues, receive unique token numbers, and track their queue status. It also supports priority-based queue management, allowing VIP or emergency customers to be served ahead of regular customers while maintaining fairness and efficiency.

The application provides real-time queue operations, token management, analytics, and role-based user management through a RESTful API architecture.

---

## Features

### Authentication & Authorization

* User Registration
* User Login
* JWT Access Token Generation
* JWT Refresh Token Generation
* Secure Password Hashing

### Queue Management

* Create New Queues
* View Available Queues
* Join a Queue
* Generate Sequential Token Numbers
* View Queue Details

### Token Management

* Automatic Token Generation
* Priority-Based Processing
* Call Next Token
* Update Token Status
* View Queue Tokens

### Analytics Dashboard

* Total Users
* Total Queues
* Total Tokens
* Active Tokens
* Completed Tokens

---

## Technology Stack

### Backend

* FastAPI
* Python 3

### Database

* PostgreSQL

### ORM

* SQLAlchemy

### Validation

* Pydantic

### Authentication

* JWT (JSON Web Tokens)
* Passlib Password Hashing

### API Documentation

* Swagger UI
* OpenAPI

### Version Control

* Git
* GitHub

---

## Database Design

The system consists of three main entities:

### User

Stores registered users and their roles.

### Queue

Stores queue information and service details.

### Token

Stores generated queue tokens, priority levels, and service status.

Relationships:

* One User can have multiple Tokens.
* One Queue can contain multiple Tokens.
* Each Token belongs to one User and one Queue.

---

## Data Structures and Algorithms Used

### FIFO Queue

Regular customers are served in First-In-First-Out order.

### Priority Queue

High-priority customers are served before normal customers.

### Sorting

Tokens are ordered based on:

1. Priority Level
2. Arrival Time

### Sequential Token Generation

Token numbers are generated automatically in sequence (A001, A002, A003, etc.).

---

## API Endpoints

### Authentication

* POST /signup
* POST /login
* GET /users

### Queue Management

* POST /queues
* GET /queues
* GET /queues/{queue_id}

### Token Management

* POST /queues/{queue_id}/join
* GET /tokens/{token_id}
* GET /queues/{queue_id}/tokens
* POST /queues/{queue_id}/call-next
* PUT /tokens/{token_id}/status

### Analytics

* GET /analytics/dashboard

---

## Future Enhancements

* Frontend Dashboard
* Email Notifications
* SMS Notifications
* QR Code Based Tokens
* Live Queue Tracking
* Multi-Branch Queue Management
* Real-Time WebSocket Updates

---

## Author

Mansi Ahirrao

Computer Science Engineering (Big Data & Cloud Engineering)

MIT ADT University, Pune
