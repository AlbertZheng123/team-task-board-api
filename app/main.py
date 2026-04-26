from __future__ import annotations

from enum import Enum
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"
    print("hey")


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(BaseModel):
    id: str
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(default="", max_length=500)
    assignee: str = Field(default="Unassigned", max_length=80)
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.todo


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(default="", max_length=500)
    assignee: str = Field(default="Unassigned", max_length=80)
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(BaseModel):
    assignee: Optional[str] = Field(default=None, max_length=80)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None


app = FastAPI(title="Team Task Board API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TASKS: list[Task] = [
    Task(
        id="task-1",
        title="Finalize onboarding checklist",
        description="Review the first-day checklist for new engineering hires.",
        assignee="Avery",
        priority=TaskPriority.high,
        status=TaskStatus.in_progress,
    ),
    Task(
        id="task-2",
        title="Polish sprint demo deck",
        description="Tighten the slides and screenshots for the Friday demo.",
        assignee="Jordan",
        priority=TaskPriority.medium,
        status=TaskStatus.todo,
    ),
    Task(
        id="task-3",
        title="Archive completed bug tickets",
        description="Move completed bug fixes into the shipped column.",
        assignee="Priya",
        priority=TaskPriority.low,
        status=TaskStatus.done,
    ),
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return TASKS


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    task = Task(id=str(uuid4()), **payload.model_dump())
    TASKS.append(task)
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    for index, task in enumerate(TASKS):
        if task.id != task_id:
            continue
        updated = task.model_copy(update=payload.model_dump(exclude_none=True))
        TASKS[index] = updated
        return updated
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/summary")
def get_summary() -> dict[str, int]:
    visible_tasks = [task for task in TASKS if task.status != TaskStatus.archived]

    return {
        "total": len(visible_tasks),
        "todo": sum(task.status == TaskStatus.todo for task in visible_tasks),
        "in_progress": sum(task.status == TaskStatus.in_progress for task in visible_tasks),
        "done": sum(task.status == TaskStatus.done for task in visible_tasks),
    }
