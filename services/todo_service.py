from domain.todo_list import TodoList, TodoStatus
from db.models import TodoListModel, UserModel
from domain.user import User
from db.uow import UnitOfWork


class TodoService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create_todo_list(self, user: User, list_name: str) -> TodoList:
        todo_list_model = TodoListModel(
            name=list_name,
            status=TodoStatus.PENDING.value,
            user_id=user.id,
        )

        self.uow.session.add(todo_list_model)
        return TodoList.from_model(todo_list_model)

    def add_item_to_list(self, user: User) -> User:
        user_model = UserModel(
            name=user.name,
            email=user.email,
        )

        self.uow.session.add(user_model)
        return User.from_model(user_model)

    def update(self, user: User) -> User:
        user_model = self.uow.session.query(UserModel).filter(UserModel.id == user.id).first()

        if user_model:
            user_model.name = user.name
            user_model.email = user.email

        self.uow.session.add(user_model)
        return user
