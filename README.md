# Python HTTP API

A modern, fast, and robust HTTP API built with FastAPI and Python. This project provides a solid foundation for building RESTful APIs with common patterns and best practices.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Automatic Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Data Validation**: Request/response validation with Pydantic
- **Environment Configuration**: Flexible configuration management
- **Testing Suite**: Comprehensive tests with pytest
- **Code Quality**: Pre-configured linting and formatting tools
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Modular Structure**: Clean, scalable project organization

## Project Structure

```
├── app/
│   ├── api/
│   │   └── endpoints/          # API route definitions
│   │       ├── health.py       # Health check endpoints
│   │       └── users.py        # User management endpoints
│   ├── core/
│   │   └── config.py          # Application configuration
│   └── models/
│       └── user.py            # Pydantic models
├── tests/                     # Test files
│   ├── conftest.py           # Test configuration
│   ├── test_health.py        # Health endpoint tests
│   └── test_users.py         # User endpoint tests
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Project configuration
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CamaraApplicationEndpointRegistration
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env` file and update values as needed
   - Update `SECRET_KEY` for production use

5. **Run the application**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Available Endpoints

### Health Check
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health information

### User Management
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py

# Run tests with verbose output
pytest -v
```

## Development

### Code Quality

The project includes tools for maintaining code quality:

```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Type check with mypy
mypy app/ tests/
```

### Adding New Endpoints

1. Create a new router file in `app/api/endpoints/`
2. Define your endpoints using FastAPI decorators
3. Add Pydantic models in `app/models/` if needed
4. Include the router in `main.py`
5. Add tests in the `tests/` directory

### Environment Variables

Key environment variables in `.env`:

- `DEBUG`: Enable debug mode (True/False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `SECRET_KEY`: Secret key for security (change in production!)
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: CORS allowed hosts (comma-separated)

## Production Deployment

### Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Manual Deployment

1. Set environment variables for production
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Common Libraries Included

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Requests & HTTPX**: HTTP clients
- **Pytest**: Testing framework
- **Black & isort**: Code formatting
- **MyPy**: Static type checking
- **SQLAlchemy**: Database ORM (optional)
- **python-jose**: JWT handling
- **passlib**: Password hashing

## Next Steps

- Add database integration (PostgreSQL, MySQL, etc.)
- Implement authentication and authorization
- Add logging and monitoring
- Set up CI/CD pipeline
- Add rate limiting
- Implement caching
- Add background tasks with Celery