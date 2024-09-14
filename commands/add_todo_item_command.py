from dataclasses import dataclass
from commands.exceptions import TodoListNotFound
from db.enum import AuditOperation
from db.models import TodoItem, TodoList
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository


@dataclass
class AddTodoItemCommandRequest:
    list_id: int
    description: str


class AddTodoItemCommand:
    def __init__(
        self,
        todo_repository: TodoRepository,
        audit_repository: AuditRepository,
    ) -> None:
        self.todo_repository = todo_repository
        self.audit_repository = audit_repository

    def run(self, request: AddTodoItemCommandRequest) -> TodoItem:
        todo_list = self.todo_repository.get_list(list_id=request.list_id)
        if not todo_list:
            raise TodoListNotFound(request.list_id)

        todo_item = TodoItem(list_id=todo_list.id, description=request.description)
        self.todo_repository.upsert_item(todo_item)
        self.audit_repository.audit(
            operation=AuditOperation.INSERT,
            user_id=todo_list.user_id,
            message=f"Adding new item '{request.description}' to the list '{todo_list.name}'",
        )
        return todo_item
