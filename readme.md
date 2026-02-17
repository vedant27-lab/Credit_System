Loan Credit Approval System

A production-ready backend system for managing customer credit profiles, evaluating loan eligibility, and processing loan creation using rule-based credit scoring.

This project is built with Django, Django REST Framework, PostgreSQL, Redis, Celery, and Docker.

🚀 Tech Stack

Backend: Django 6 + Django REST Framework

Database: PostgreSQL

Task Queue: Celery

Message Broker: Redis

Containerization: Docker + Docker Compose

📦 Architecture

The system follows a service-based backend architecture:

Django API
   │
   ├── PostgreSQL (Primary Database)
   │
   └── Redis (Message Broker)
           │
           └── Celery Worker (Background Tasks)


Django handles API logic and business rules.

PostgreSQL stores customers and loan records.

Redis manages background task communication.

Celery processes async tasks like bulk data ingestion.

📌 Features
1. Customer Registration

Registers new customers

Automatically calculates approved credit limit

Uses auto-incrementing primary keys

2. Credit Score Calculation

Score is computed using:

Repayment ratio

Number of loans

Loan activity in current year

Loan volume vs approved limit

3. Loan Eligibility Check

Evaluates:

Credit score thresholds

Corrected interest rates

EMI calculation

50% salary EMI burden rule

4. Loan Creation

Creates loan only if eligibility rules pass

Stores monthly installment and repayment details

5. Loan Viewing

View individual loan

View all loans of a customer

6. Background Data Ingestion

Uses Celery for async Excel ingestion

Runs without blocking API

🛠 Setup Instructions
Prerequisites

Docker Desktop installed and running

🐳 Run With Docker

From the directory containing docker-compose.yml:

docker compose up --build


This will start:

PostgreSQL container

Redis container

Django application

Celery worker

Run Migrations
docker compose exec web python manage.py migrate

Create Superuser (Optional)
docker compose exec web python manage.py createsuperuser

🌐 API Endpoints
Register Customer
POST /api/register/


Request:

{
  "first_name": "John",
  "last_name": "Doe",
  "age": 25,
  "phone_number": "9876543210",
  "monthly_salary": 50000
}

Check Loan Eligibility
POST /api/check-eligibility/

Create Loan
POST /api/create-loan/

View Single Loan
GET /api/view-loan/<loan_id>/

View Customer Loans
GET /api/view-loans/<customer_id>/

🧠 Business Rules
Approved Limit
Approved Limit = Monthly Salary × 36

EMI Rule

Total EMI burden must not exceed 50% of monthly salary.

Interest Rate Correction

Based on credit score tiers.

Credit Score Components

Repayment behavior

Loan count

Recent loan activity

Loan-to-limit ratio

📂 Project Structure
creditSystem/
│
├── customers/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tasks.py
│
├── loans/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
│
├── core/
│   └── services/
│       ├── credit_score.py
│       ├── eligibility.py
│       └── emi.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

🔄 Background Worker

Celery worker runs as a separate container:

Broker: Redis

Triggered via API

Processes async ingestion tasks

🧪 Testing Strategy

The system supports:

Manual API testing via Postman

Container-level testing

Migration validation via Docker

Background task verification through Celery logs

📈 Production Readiness

This system supports:

Scalable database architecture (PostgreSQL)

Async background processing

Service separation

Containerized deployment

Clean REST API design

📝 Notes

Primary keys are auto-managed by Django.

Database is reset using docker compose down -v.

Redis and PostgreSQL communicate internally within Docker network.

No hardcoded localhost dependencies inside containers.

🏁 Final Status

Fully functional API

Dockerized services

PostgreSQL integrated

Celery + Redis working

Clean separation of concerns