from dataclasses import dataclass
from db.enum import AuditOperation
from db.models import TodoList, User
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository


@dataclass
class AddUserCommandRequest:
    first_name: str
    last_name: str
    email: str
    default_list_name: str


class AddUserCommand:
    def __init__(
        self,
        user_repository: UserRepository,
        todo_repository: TodoRepository,
        audit_repository: AuditRepository,
    ) -> None:
        self.user_repository = user_repository
        self.todo_repository = todo_repository
        self.audit_repository = audit_repository

    def run(self, request: AddUserCommandRequest) -> User:
        user = self.user_repository.upsert(
            User(first_name=request.first_name, last_name=request.last_name, email=request.email)
        )
        self.audit_repository.audit(
            operation=AuditOperation.INSERT,
            user_id=user.id,
            message=f"Adding new user {user.first_name} {user.last_name} <{user.email}>",
        )
        todo_list = self.todo_repository.upsert_list(TodoList(name=request.default_list_name, user_id=user.id))
        self.audit_repository.audit(
            operation=AuditOperation.INSERT, user_id=user.id, message=f"Adding new list '{todo_list.name}'"
        )
        return user
