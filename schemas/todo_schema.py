from __future__ import annotations
import datetime
from pydantic import BaseModel
from domain.todo_list import TodoStatus


class TodoListRequest(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "My List",
            }
        }


class TodoListResponse(BaseModel):
    id: int
    name: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime


class TodoItemRequest(BaseModel):
    list_id: int
    description: str

    class Config:
        schema_extra = {
            "example": {
                "list_id": 1,
                "description": "My item",
            }
        }


class TodoItemResponse(BaseModel):
    id: int
    description: str
    status: TodoStatus
    list_id: int
    created: datetime.datetime
    updated: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "description": "My item",
                "list_id": 1,
            }
        }
