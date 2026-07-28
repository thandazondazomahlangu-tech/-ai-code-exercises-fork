from datetime import date
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from ..models.todo import TodoCreate, TodoResponse, TodoUpdate
from ..utils.exceptions import TodoNotFoundError

router = APIRouter(prefix="/todos", tags=["todos"])

fake_todos_db: Dict[int, Dict] = {}
next_todo_id = 1


def _get_todo_or_raise(todo_id: int) -> Dict:
    todo = fake_todos_db.get(todo_id)
    if todo is None:
        raise TodoNotFoundError(todo_id)
    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    global next_todo_id
    todo_id = next_todo_id
    next_todo_id += 1

    todo_data = todo.dict()
    todo_data.update({"id": todo_id, "completed": False})
    fake_todos_db[todo_id] = todo_data

    return todo_data


@router.get("/", response_model=List[TodoResponse])
async def list_todos(status: Optional[str] = Query(None, description="Filter by status: completed or pending")):
    todos = list(fake_todos_db.values())
    if status is not None:
        status_lower = status.lower()
        if status_lower == "completed":
            todos = [todo for todo in todos if todo["completed"]]
        elif status_lower == "pending":
            todos = [todo for todo in todos if not todo["completed"]]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status filter must be 'completed' or 'pending'"
            )
    return todos


@router.patch("/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(
    todo_id: int = Path(..., gt=0, description="ID of the to-do item to mark completed")
):
    todo = _get_todo_or_raise(todo_id)
    todo["completed"] = True
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int = Path(..., gt=0, description="ID of the to-do item to delete")
):
    _get_todo_or_raise(todo_id)
    del fake_todos_db[todo_id]
    return None
