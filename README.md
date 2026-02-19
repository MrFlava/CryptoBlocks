# CryptoBlocks project

A modern FastAPI application with Django ORM, Celery task queue, and JWT authentication.

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Setup & Run

1. **Clone and start:**
```bash
git clone <repository-url>
cd fastapi-django-template
docker-compose up --build
```

2. **Access the application:**
- **FastAPI App:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Django Admin:** http://localhost:8000/django/admin

## API Endpoints

### Authentication
- **Login:** `POST /auth/login`
  ```bash
  curl -X POST "http://localhost:8000/auth/login" \
    -d "username=your@email.com" \
    -d "password=yourpassword"
  ```

### User Management
- **Public Registration:** `POST /user/register`
  ```bash
  curl -X POST "http://localhost:8000/user/register" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
  ```

- **Admin Account Creation:** `POST /user/accounts` (Admin only)
- **Get Current User:** `GET /user/` (Authenticated)

### Blockchain Data
- **List Blocks:** `GET /crypto/api/v1/blocks`
  ```bash
  curl -X GET "http://localhost:8000/crypto/api/v1/blocks?page=1&page_size=10" \
    -H "Authorization: Bearer YOUR_TOKEN"
  ```

- **Get Block by ID:** `GET /crypto/api/v1/blocks/{id}`
- **Get Block by Currency:** `GET /crypto/api/v1/blocks/by-currency/{currency}/{number}`
- **List Providers:** `GET /crypto/api/v1/providers`
- **List Currencies:** `GET /crypto/api/v1/currencies`

### Health Check
- **Status:** `GET /health/status`

## Features

- **JWT Authentication** with role-based access control
- **Async Django ORM** for database operations
- **Celery** for background task processing
- **Redis** for caching and message broker
- **Pagination & Filtering** for blockchain data
- **Auto-generated API docs** with Swagger UI

## Development

### Project Structure
```
fastapi/
├── app/
│   ├── api/          # Business logic
│   ├── models/       # Django models
│   ├── routers/     # FastAPI routes
│   ├── schemas/      # Pydantic models
│   └── dependencies/ # Auth dependencies
├── workers/         # Celery tasks
└── config/          # Django & FastAPI config
```

### Database Migrations
```bash
docker-compose exec fastapi python manage.py makemigrations
docker-compose exec fastapi python manage.py migrate
```

### Create Superuser
```bash
docker-compose exec fastapi python manage.py createsuperuser
```

## Testing

Run the test script to verify all endpoints:
```bash
python test_endpoints.py
```

## Environment Variables

Key environment variables in `docker-compose.yml`:
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `SECRET_KEY` - JWT signing key

## Support

For issues and questions, check the API documentation at http://localhost:8000/docs
