from domain.todo_list import TodoStatus
from db.models import TodoListModel, TodoItemModel
from db.uow import UnitOfWork


class TodoRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def create_todo_list(self, user_id: int, list_name: str) -> TodoListModel:
        todo_list_model = TodoListModel(
            name=list_name,
            status=TodoStatus.PENDING.value,
            user_id=user_id,
        )

        self.uow.session.add(todo_list_model)
        self.uow.session.flush()
        return todo_list_model

    def add_item_to_list(
        self,
        list_model: TodoListModel,
        description: str,
    ) -> TodoItemModel:
        list_model.items.append(
            TodoItemModel(
                description=description,
                status=TodoStatus.PENDING.value,
            )
        )
        list_model.save()
        item = TodoItemModel(
            list_id=list_id,
            description=description,
            status=TodoStatus.PENDING.value,
        )

        self.uow.session.add(item)
        self.uow.session.flush()
        return item

    def complete_item(self, item_id: int) -> TodoItemModel:
        item = self.uow.session.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()

        if not item:
            raise ValueError("Item not found")

        if item.status == TodoStatus.COMPLETED.value:
            return item

        item.status = TodoStatus.COMPLETED.value
        self.uow.session.add(item)
        self.uow.session.flush()
        return item

    # def update(self, user: User) -> User:
    #     user_model = self.uow.session.query(UserModel).filter(UserModel.id == user.id).first()

    #     if user_model:
    #         user_model.name = user.name
    #         user_model.email = user.email

    #     self.uow.session.add(user_model)
    #     return user
