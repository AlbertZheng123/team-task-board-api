# Team Task Board API

A small FastAPI backend for a team task board demo app. This repo exposes a simple in-memory REST API for listing, creating, and updating task items.

## Features

- Health check endpoint
- List tasks
- Create tasks
- Update task status and assignee
- Summary endpoint for lightweight dashboard metrics
- CORS enabled for local frontend development

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn

## Project Structure

```text
team-task-board-api/
├── app/
│   └── main.py
├── tests/
│   └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will start on `http://localhost:8000`.

## Endpoints

- `GET /health`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `GET /summary`

## Example Request

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Draft launch checklist",
    "description": "Prepare a first-pass release checklist for the beta launch.",
    "assignee": "Mia",
    "priority": "high"
  }'
```

## Running Tests

```bash
pytest
```
