from __future__ import annotations
import datetime
from pydantic import BaseModel
from commands.add_todo_item_command import AddTodoItemCommandRequest
from commands.add_todo_list_command import AddTodoListCommandRequest
from db.models import TodoItem, TodoList, TodoStatus


class TodoListRequest(BaseModel):
    user_id: int
    list_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "list_name": "My List",
            }
        }

    def to_command_request(self) -> AddTodoListCommandRequest:
        return AddTodoListCommandRequest(user_id=self.user_id, list_name=self.list_name)


class TodoListResponse(BaseModel):
    id: int
    name: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime
    items: list[TodoItemResponse]

    @staticmethod
    def from_todo_list(todo_list: TodoList) -> TodoListResponse:
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

    def to_command_request(self, list_id: int) -> AddTodoItemCommandRequest:
        return AddTodoItemCommandRequest(list_id=list_id, description=self.description)


class TodoItemResponse(BaseModel):
    id: int
    description: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime

    @staticmethod
    def from_todo_item(todo_item: TodoItem) -> TodoItemResponse:
        return TodoItemResponse(
            id=todo_item.id,
            description=todo_item.description,
            status=todo_item.status,
            created=todo_item.created,
            updated=todo_item.updated,
        )
