# Task Management API

A Flask-based RESTful API for managing tasks and comments.

## Features

- Task CRUD operations
- Comment CRUD operations linked to tasks
- SQLAlchemy ORM with SQLite database
- Comprehensive test coverage with pytest

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Tasks

- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks
- `GET /tasks/<task_id>` - Get a specific task
- `PUT /tasks/<task_id>` - Update a task
- `DELETE /tasks/<task_id>` - Delete a task

### Comments

- `POST /tasks/<task_id>/comments` - Create a comment for a task
- `GET /tasks/<task_id>/comments` - List all comments for a task
- `PUT /comments/<comment_id>` - Update a comment
- `DELETE /comments/<comment_id>` - Delete a comment

## Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Project Structure

```
Better/
├── app.py                 # Application entry point
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── routes/
│   ├── task_routes.py    # Task endpoints
│   └── comment_routes.py # Comment endpoints
└── tests/
    ├── conftest.py       # Test configuration
    ├── test_tasks.py     # Task tests
    └── test_comments.py  # Comment tests
```
