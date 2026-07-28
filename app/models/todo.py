from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="The title of the to-do item")
    description: Optional[str] = Field(None, max_length=500, description="Optional details about the to-do item")
    due_date: Optional[date] = Field(None, description="Optional due date for the to-do item")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=500)
    due_date: Optional[date]
    completed: Optional[bool]


class TodoResponse(TodoBase):
    id: int
    completed: bool = Field(False, description="Whether the to-do item is completed")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Finish FastAPI exercise",
                "description": "Create a simple to-do list API with CRUD operations",
                "due_date": "2026-08-01",
                "completed": False
            }
        }
