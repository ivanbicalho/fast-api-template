from db.models import TodoList, TodoItem
from db.uow import UnitOfWork


class TodoRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def get_list(self, list_id: int) -> TodoList | None:
        return self._uow.session.query(TodoList).join(TodoItem, TodoList.items).filter(TodoList.id == list_id).first()

    def get_list_from_item(self, item_id: int) -> TodoList | None:
        return self._uow.session.query(TodoList).join(TodoItem, TodoList.items).filter(TodoItem.id == item_id).first()

    def upsert_list(self, todo_list: TodoList) -> TodoList:
        self._uow.session.add(todo_list)
        self._uow.session.flush()
        return todo_list

    def upsert_item(self, todo_item: TodoItem) -> TodoItem:
        self._uow.session.add(todo_item)
        self._uow.session.flush()
        return todo_item
