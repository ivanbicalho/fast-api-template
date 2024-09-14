from dataclasses import dataclass
from commands.exceptions import UserNotFound
from db.enum import AuditOperation
from db.models import TodoList
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository


@dataclass
class AddTodoListCommandRequest:
    user_id: int
    list_name: str


class AddTodoListCommand:
    def __init__(
        self,
        user_repository: UserRepository,
        todo_repository: TodoRepository,
        audit_repository: AuditRepository,
    ) -> None:
        self.user_repository = user_repository
        self.todo_repository = todo_repository
        self.audit_repository = audit_repository

    def run(self, request: AddTodoListCommandRequest) -> TodoList:
        user = self.user_repository.get_user(request.user_id)
        if not user:
            raise UserNotFound(request.user_id)

        todo_list = self.todo_repository.upsert_list(TodoList(name=request.list_name, user_id=user.id))
        self.audit_repository.audit(
            operation=AuditOperation.INSERT, user_id=request.user_id, message=f"Adding new list '{todo_list.name}'"
        )
        return todo_list
