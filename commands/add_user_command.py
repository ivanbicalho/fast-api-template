from dataclasses import dataclass
from db.enum import AuditOperation
from db.models import TodoListModel, UserModel
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository


@dataclass
class AddUserUseCaseRequest:
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

    def run(self, request: AddUserUseCaseRequest) -> UserModel:
        user = self.user_repository.upsert(
            UserModel(first_name=request.first_name, last_name=request.last_name, email=request.email)
        )
        self.todo_repository.upsert_list(TodoListModel(name=request.default_list_name, user_id=user.id))
        self.audit_repository.audit(
            AuditOperation.INSERT, f"Adding new user {user.first_name} {user.last_name} <{user.email}>"
        )
        return user
