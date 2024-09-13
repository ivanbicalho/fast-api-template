from db.models import AuditModel, TodoListModel, TodoItemModel
from db.uow import UnitOfWork


class TodoRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def get_list(self, list_id: int) -> TodoListModel:
        return (
            self.uow.session.query(TodoListModel).add_entity(TodoItemModel).filter(TodoListModel.id == list_id).first()
        )

    def upsert_list(self, todo_list: TodoListModel) -> TodoListModel:
        if todo_list.id:
            audit = AuditModel(operation="update", message=f"Updating list {todo_list.id}")
        else:
            audit = AuditModel(
                operation="insert", message=f"Adding new list {todo_list.name} from user {todo_list.user_id}"
            )

        self.uow.session.add(audit)
        self.uow.session.add(todo_list)
        self.uow.session.flush()
        return todo_list

    def upsert_item(self, todo_item: TodoItemModel) -> TodoItemModel:
        if todo_item.id:
            audit = AuditModel(operation="update", message=f"Updating {todo_item.id}")
        else:
            audit = AuditModel(
                operation="insert", message=f"Adding new item '{todo_item.description}' to list {todo_item.list_id}"
            )

        self.uow.session.add(audit)
        self.uow.session.add(todo_item)
        self.uow.session.flush()
        return todo_item

    # def complete_item(self, item_id: int) -> TodoItemModel:
    #     item = self.uow.session.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()

    #     if not item:
    #         raise ValueError("Item not found")

    #     if item.status == TodoStatus.COMPLETED.value:
    #         return item

    #     item.status = TodoStatus.COMPLETED.value
    #     self.uow.session.add(item)
    #     self.uow.session.flush()
    #     return item
