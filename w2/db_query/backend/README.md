# Database Query Tool - Backend

FastAPI backend for managing database connections and executing SQL queries with natural language support.

## Tech Stack

- **Python 3.12+**: Modern Python with type hints
- **FastAPI**: High-performance web framework with automatic API documentation
- **SQLModel**: ORM built on Pydantic and SQLAlchemy
- **sqlglot**: SQL parser and validator
- **asyncpg**: Async PostgreSQL driver
- **aiomysql/PyMySQL**: Async MySQL driver
- **Google Generative AI SDK**: Natural language to SQL conversion using Gemini
- **Alembic**: Database migrations
- **pytest**: Testing framework

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- PostgreSQL or MySQL database for testing (optional, for connection testing)

## Setup

### 1. Install Dependencies

Using uv (recommended):

```bash
cd backend
uv sync --extra dev
```

Using pip:

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Configure Environment

Copy `.env.example` to `.env` and set your Google Gemini API key:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

Required environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key for natural language to SQL feature (get it from https://makersuite.google.com/app/apikey)
- `DB_QUERY_DATA_DIR`: (Optional) Directory for SQLite database (default: `~/.db_query`)
- `LOG_LEVEL`: (Optional) Logging level (default: `INFO`)

### 3. Initialize Database

Run database migrations:

```bash
uv run alembic upgrade head
# or with pip:
alembic upgrade head
```

### 4. Start Development Server

```bash
uv run uvicorn app.main:app --reload --port 8000
# or with pip:
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Usage Examples

### 1. Create Database Connection

```bash
curl -X PUT "http://localhost:8000/api/v1/dbs/my-postgres" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "postgresql://user:password@localhost:5432/mydb",
    "dbType": "postgresql",
    "description": "Local PostgreSQL database"
  }'
```

**Response:**
```json
{
  "name": "my-postgres",
  "url": "postgresql://user:password@localhost:5432/mydb",
  "dbType": "postgresql",
  "description": "Local PostgreSQL database",
  "createdAt": "2025-01-01T12:00:00Z",
  "updatedAt": "2025-01-01T12:00:00Z",
  "lastConnectedAt": null,
  "status": "active"
}
```

### 2. List All Connections

```bash
curl "http://localhost:8000/api/v1/dbs"
```

### 3. Get Database Metadata

```bash
curl "http://localhost:8000/api/v1/dbs/my-postgres"
```

To refresh metadata:

```bash
curl "http://localhost:8000/api/v1/dbs/my-postgres?refresh=true"
```

### 4. Execute SQL Query

```bash
curl -X POST "http://localhost:8000/api/v1/dbs/my-postgres/query" \
  -H "Content-Type: application/json" \
  -d '{
    "sql": "SELECT id, name, email FROM users LIMIT 10"
  }'
```

**Response:**
```json
{
  "columns": [
    {"name": "id", "dataType": "integer"},
    {"name": "name", "dataType": "character varying"},
    {"name": "email", "dataType": "character varying"}
  ],
  "rows": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
  ],
  "rowCount": 2,
  "executionTimeMs": 45,
  "sql": "SELECT id, name, email FROM users LIMIT 10"
}
```

### 5. Natural Language to SQL

```bash
curl -X POST "http://localhost:8000/api/v1/dbs/my-postgres/query/natural" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Show me all users who signed up this month"
  }'
```

**Response:**
```json
{
  "sql": "SELECT * FROM users WHERE created_at >= date_trunc('month', CURRENT_DATE) LIMIT 1000",
  "explanation": "Generated SQL to find all users created in the current month"
}
```

**Rate Limiting**: The natural language endpoint has rate limiting (default: 10 requests per 60 seconds per IP). If exceeded, you'll receive a `429 Too Many Requests` response.

### 6. Get Query History

```bash
curl "http://localhost:8000/api/v1/dbs/my-postgres/history?limit=10"
```

### 7. Delete Database Connection

```bash
curl -X DELETE "http://localhost:8000/api/v1/dbs/my-postgres"
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_sql_validator.py
```

### Code Quality

```bash
# Type checking
uv run mypy app

# Linting
uv run ruff check app

# Format code
uv run ruff format app
```

### Database Migrations

```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   │   ├── databases.py # Database connection management
│   │   └── queries.py   # Query execution
│   ├── models/          # Pydantic models and SQLModel entities
│   ├── services/        # Business logic
│   │   ├── db_connection.py
│   │   ├── metadata.py
│   │   ├── query.py
│   │   ├── sql_validator.py
│   │   ├── nl2sql.py
│   │   └── rate_limiter.py
│   ├── adapters/        # Database adapter pattern
│   ├── config.py        # Configuration (Pydantic Settings)
│   ├── database.py      # SQLite database setup
│   └── main.py          # FastAPI application
├── alembic/             # Database migrations
├── tests/               # Test suite
├── pyproject.toml       # Project dependencies
└── alembic.ini          # Alembic configuration
```

## Configuration

Configuration is managed via Pydantic Settings in `app/config.py`. All settings can be overridden via environment variables:

- `GEMINI_API_KEY`: Required for natural language features (Google Gemini API key)
- `DB_QUERY_DATA_DIR`: SQLite database directory (default: `~/.db_query`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `CORS_ORIGINS`: CORS allowed origins (default: `*`)
- `QUERY_DEFAULT_LIMIT`: Default query row limit (default: `1000`)
- `LLM_RATE_LIMIT_MAX_REQUESTS`: Rate limit max requests (default: `10`)
- `LLM_RATE_LIMIT_WINDOW_SECONDS`: Rate limit window (default: `60`)

## Features

### SQL Validation

- Only SELECT statements allowed
- Automatic LIMIT injection (if missing)
- Multi-statement queries blocked
- Dangerous functions blocked (e.g., `pg_read_file`, `COPY`)

### Metadata Caching

- Metadata fetched from PostgreSQL/MySQL system tables
- Cached in SQLite for 24 hours (configurable)
- Manual refresh via API parameter

### Rate Limiting

- Natural language endpoint protected by rate limiter
- In-memory sliding window algorithm
- Configurable limits via environment variables

## Troubleshooting

### Database Connection Issues

1. Verify connection URL format:
   - PostgreSQL: `postgresql://user:password@host:port/database`
   - MySQL: `mysql://user:password@host:port/database`

2. Check network connectivity and firewall rules

3. Verify database credentials

### Gemini API Issues

1. Ensure `GEMINI_API_KEY` is set in `.env`
2. Check API key validity (get it from https://makersuite.google.com/app/apikey)
3. Verify internet connectivity
4. Ensure you have access to Google's Gemini API

### Migration Issues

If database schema is out of sync:

```bash
# Check current revision
uv run alembic current

# View migration history
uv run alembic history

# Reset database (WARNING: deletes all data)
rm ~/.db_query/db_query.db
uv run alembic upgrade head
```

## License

See root README for license information.

