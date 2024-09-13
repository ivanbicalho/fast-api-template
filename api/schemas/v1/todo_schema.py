from __future__ import annotations
import datetime
from pydantic import BaseModel
from db.models import TodoItemModel, TodoListModel, TodoStatus


class TodoListRequest(BaseModel):
    user_id: int
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "name": "My List",
            }
        }

    def to_todo_list(self) -> TodoListModel:
        return TodoListModel(name=self.name, user_id=self.user_id)


class TodoListResponse(BaseModel):
    id: int
    name: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime
    items: list[TodoItemResponse]

    @staticmethod
    def from_todo_list(todo_list: TodoListModel) -> TodoListResponse:
        return TodoListResponse(
            id=todo_list.id,
            name=todo_list.name,
            status=todo_list.status,
            created=todo_list.created,
            updated=todo_list.updated,
            items=[TodoItemResponse.from_todo_item(item) for item in todo_list.items],
        )


class TodoItemRequest(BaseModel):
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "description": "My item",
            }
        }

    def to_todo_item(self, list_id: int) -> TodoItemModel:
        return TodoItemModel(description=self.description, list_id=list_id)


class TodoItemResponse(BaseModel):
    id: int
    description: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime

    @staticmethod
    def from_todo_item(todo_item: TodoItemModel) -> TodoItemResponse:
        return TodoItemResponse(
            id=todo_item.id,
            description=todo_item.description,
            status=todo_item.status,
            created=todo_item.created,
            updated=todo_item.updated,
        )
