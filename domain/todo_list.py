from __future__ import annotations
from dataclasses import dataclass
import datetime
from enum import Enum

from db.models import TodoItemModel, TodoListModel


class TodoStatus(Enum):
    PENDING = 0
    COMPLETED = 1


@dataclass
class TodoList:
    id: int
    name: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime

    @staticmethod
    def from_model(model: TodoListModel) -> TodoList:
        return TodoList(
            id=model.id,
            name=model.name,
            status=TodoStatus(model.status),
            created=model.created,
            updated=model.updated,
        )


@dataclass
class TodoItem:
    list_id: int
    id: int
    description: str
    status: TodoStatus
    created: datetime.datetime
    updated: datetime.datetime

    @staticmethod
    def from_model(model: TodoItemModel) -> TodoItem:
        return TodoItem(
            list_id=model.list_id,
            id=model.id,
            description=model.description,
            status=TodoStatus(model.status),
            created=model.created,
            updated=model.updated,
        )
