# PyConf Hyderabad 2025 - TDD Workshop

A project demonstrating Test Driven Development in Django with factory_boy and faker, created for the PyConf Hyderabad 2025 workshop.

## Project Overview

This is a Todo List API built with Django REST Framework that includes:

- User authentication with JWT tokens
- Todo list and item management
- Filtering, searching and ordering capabilities
- Admin interface customization
- Comprehensive test coverage

## Getting Started

### Prerequisites
- Python 3.12 or higher
- Poetry for dependency management
- SQLite (default database)

### First Time Setup

1. Clone the repository
```bash
git clone https://github.com/kdpisda/pyconf-hyd-2025
cd pyconf-hyd-2025
```

2. Install Poetry if you haven't already
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies
```bash
poetry install
```

4. Activate the virtual environment
```bash
poetry shell
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

7. Start the development server
```bash
python manage.py runserver
```

The API will be available at http://localhost:8000

### Running Tests
```bash
pytest
```

For test coverage report:
```bash
pytest --cov
```

## API Endpoints

### Authentication
- POST `/auth/register/` - Register new user
- POST `/auth/login/` - Obtain JWT token
- POST `/auth/refresh/` - Refresh JWT token

### Todo Lists
- GET `/todo/lists/` - List all todo lists
- POST `/todo/lists/` - Create new todo list
- GET `/todo/lists/{id}/` - Retrieve specific list
- PUT `/todo/lists/{id}/` - Update list
- PATCH `/todo/lists/{id}/` - Partial update list

### Todo Items
- GET `/todo/items/` - List all items
- POST `/todo/items/` - Create new item
- GET `/todo/items/{id}/` - Retrieve specific item
- PUT `/todo/items/{id}/` - Update item
- PATCH `/todo/items/{id}/` - Partial update item

## Features

### Authentication
- JWT based authentication
- User registration with validation
- Token refresh mechanism

### Todo Lists
- Create and manage multiple todo lists
- Each list belongs to a user
- List title and description

### Todo Items
- Create items within lists
- Set priority (Low/Medium/High)
- Due dates with validation
- Mark items as completed
- Rich filtering and search capabilities

### Admin Interface
- Custom admin views for Lists and Items
- Priority color coding
- Due date status indicators
- User-specific data access

## Development

### Code Quality Tools
The project uses several code quality tools:

- Black for code formatting
- Flake8 for linting
- pre-commit hooks for automated checks

To set up pre-commit hooks:
```bash
pre-commit install
```

## Project Structure
```
pyconf-hyd-2025/
├── authentication/     # User authentication app
├── todo/              # Main todo application
├── pyconfhyd/         # Project configuration
├── tests/             # Test files
└── manage.py          # Django management script
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Install development dependencies
4. Run tests to ensure everything works
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Workshop Details

This project is part of the "Mastering Test Driven Development in Django" workshop at PyConf Hyderabad 2025. For workshop materials and slides, please visit [workshop link].

## Author

Kuldeep Pisda (hello@kdpisda.in)
