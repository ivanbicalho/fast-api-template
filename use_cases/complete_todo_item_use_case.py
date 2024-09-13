from dataclasses import dataclass
from db.models import TodoListModel, UserModel
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository


class AddUserUseCase:
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    # def run(self, todo_item_id: int) -> ...:
    #     user = self.user_repository.upsert(
    #         UserModel(first_name=request.first_name, last_name=request.last_name, email=request.email)
    #     )
    #     self.todo_repository.upsert_list(TodoListModel(name=request.default_list_name, user_id=user.id))
    #     return user
