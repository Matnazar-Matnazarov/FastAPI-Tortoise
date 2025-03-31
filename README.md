# FastAPI-Tortoise

A modern web API built with FastAPI and Tortoise ORM, featuring user authentication, post management, comments, and image handling.

## Features

- 🔐 JWT Authentication
- 👤 User Management
- 📝 Posts & Comments
- ❤️ Like System
- 🖼️ Image Upload
- �� Migration Support
- 🚀 Fast Performance with uv

## Prerequisites

- Python 3.12+
- PostgreSQL

## Installation Guide

### 1. Install uv (Fast Python Package Installer)

```bash
# Install uv using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### 2. Clone and Setup Project

```bash
# Clone repository
git clone https://github.com/Matnazar-Matnazarov/FastAPI-Tortoise.git
cd FastAPI-Tortoise

# Create virtual environment using uv
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate    # Windows

# Install dependencies using uv
uv pip install -r requirements.txt
```

### 3. Database Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgres://username:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Migration with Aerich

```bash
# Initialize Aerich
aerich init -t app.database.TORTOISE_ORM

# Create initial database
aerich init-db

# For new migrations
aerich migrate --name add_new_field

# Apply migrations
aerich upgrade
```

### 5. Running the Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Project Structure

```
app/
├── auth/                   # Authentication modules
│   ├── auth.py            # Authentication logic
│   ├── jwt.py             # JWT handling
│   └── __init__.py
│
├── crud/                   # Database operations
│   ├── user.py            # User CRUD operations
│   ├── post.py            # Post CRUD operations
│   ├── comment.py         # Comment CRUD operations
│   ├── likes.py           # Like system operations
│   ├── images.py          # Image handling
│   └── comment_likes.py   # Comment likes operations
│
├── models/                 # Database models
│   ├── user.py            # User model
│   ├── post.py            # Post model
│   ├── comment.py         # Comment model
│   ├── likes.py           # Likes model
│   ├── images.py          # Image model
│   └── comment_likes.py   # Comment likes model
│
├── routers/               # API routes
│   ├── user.py           # User endpoints
│   ├── post.py           # Post endpoints
│   ├── comment.py        # Comment endpoints
│   ├── likes.py          # Likes endpoints
│   ├── images.py         # Image endpoints
│   └── comment_likes.py  # Comment likes endpoints
│
├── schemas/               # Pydantic models
│   ├── user.py           # User schemas
│   ├── post.py           # Post schemas
│   ├── comment.py        # Comment schemas
│   ├── likes.py          # Likes schemas
│   ├── images.py         # Image schemas
│   └── comment_likes.py  # Comment likes schemas
│
├── config.py             # Configuration settings
├── database.py           # Database connection
├── main.py              # Application entry point
└── __init__.py

migrations/               # Database migrations
├── models/
    └── versions/        # Migration versions

config.toml              # Aerich configuration
requirements.txt         # Project dependencies
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development Commands

```bash
# Install new package
uv pip install package_name

# Update requirements.txt
uv pip freeze > requirements.txt

# Create new migration
aerich migrate --name migration_name

# Upgrade database
aerich upgrade

# Downgrade database
aerich downgrade

# Show migration history
aerich history
```

## Common Issues and Solutions

1. If you get database connection errors:
   - Check if PostgreSQL is running
   - Verify database credentials in .env file
   - Ensure database exists

2. Migration issues:
   ```bash
   # Reset migrations
   aerich downgrade -a
   rm -rf migrations
   aerich init -t app.database.TORTOISE_ORM
   aerich init-db
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

