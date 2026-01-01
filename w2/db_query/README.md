# Database Query Tool

A web-based tool for managing database connections (PostgreSQL and MySQL), viewing metadata, executing SQL queries, and converting natural language to SQL using AI.

## Project Structure

```
w2/db_query/
├── backend/          # FastAPI backend (Python 3.12+)
├── frontend/         # React frontend (TypeScript, Refine 5)
├── fixtures/         # REST Client test files
│   ├── test.rest     # API test requests
│   └── README.md     # Testing guide
└── Makefile          # Development commands
```

## Quick Start

### Initial Setup

```bash
# Install all dependencies
make install

# Setup database and environment
make setup
# Then edit backend/.env and add your GEMINI_API_KEY (get it from https://makersuite.google.com/app/apikey)

# Start development servers
make dev
```

### Development Commands

```bash
# View all available commands
make help

# Start backend only
make dev-backend

# Start frontend only
make dev-frontend

# Run tests
make test

# Format code
make format

# Run linters
make lint
```

## API Testing

### Using REST Client (VSCode)

1. Install [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
2. Open `fixtures/test.rest`
3. Click "Send Request" above any HTTP request
4. View responses in VSCode panel

See `fixtures/README.md` for detailed testing guide.

### Using Makefile

```bash
# Check if backend is running
make health

# Open API documentation
make docs
```

## Features

### ✅ Core Features (Phase 1 & 2)

- **Database Connection Management**: Add, edit, delete, and test database connections
- **Metadata Browsing**: View database schemas, tables, and columns in a tree view
- **SQL Query Execution**: Execute SELECT queries with syntax highlighting and results table
- **Query History**: View and re-run previously executed queries

### ✅ Enhanced Features (Phase 3)

- **Natural Language to SQL**: Generate SQL queries from English or Chinese natural language using Google Gemini
- **Export Results**: Export query results to CSV or JSON format
- **Rate Limiting**: Protected LLM endpoint with configurable rate limits

### 🚧 Phase 4 (In Progress)

- Documentation and testing improvements
- Developer tools configuration

## Architecture

### Backend

- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite for local storage, PostgreSQL/MySQL for query execution
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Validation**: sqlglot for SQL parsing and validation
- **AI**: Google Generative AI SDK (Gemini) for natural language to SQL conversion

### Frontend

- **Framework**: React 18 with TypeScript
- **Admin Framework**: Refine 5
- **UI Library**: Ant Design 5
- **Code Editor**: Monaco Editor (VS Code engine)
- **Styling**: Tailwind CSS 4
- **Build Tool**: Vite

## Project Status

✅ **Phase 1 Complete**: Setup and foundation  
✅ **Phase 2 Complete**: Core features (US1 + US2)  
✅ **Phase 3 Complete**: Enhanced features (US3 + US4)  
🚧 **Phase 4 In Progress**: Documentation and polish

See [PHASE3_IMPLEMENTATION.md](./PHASE3_IMPLEMENTATION.md) for detailed implementation status.

## Documentation

- **[Backend README](./backend/README.md)**: Backend setup, API usage, and development guide
- **[Frontend README](./frontend/README.md)**: Frontend setup, features, and development guide
- **[Architecture Documentation](./docs/)**: Detailed architecture and design documents
