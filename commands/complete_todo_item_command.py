from dataclasses import dataclass
from commands.exceptions import TodoItemNotFound, TodoListNotFound
from db.enum import AuditOperation, TodoStatus
from db.models import TodoItem
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository


@dataclass
class CompleteTodoItemCommandRequest:
    list_id: int
    item_id: int


class CompleteTodoItemCommand:
    def __init__(self, todo_repository: TodoRepository, audit_repository: AuditRepository) -> None:
        self.todo_repository = todo_repository
        self.audit_repository = audit_repository

    def run(self, request: CompleteTodoItemCommandRequest) -> TodoItem:
        todo_list = self.todo_repository.get_list(request.list_id)

        if not todo_list:
            raise TodoListNotFound(request.list_id)

        try:
            todo_item = next(i for i in todo_list.items if i.id == request.item_id)
        except StopIteration:
            raise TodoItemNotFound(request.item_id)

        if todo_item.status == TodoStatus.COMPLETED:
            # return the item if it's already completed
            return todo_item

        todo_item.status = TodoStatus.COMPLETED
        self.audit_repository.audit(
            AuditOperation.UPDATE,
            todo_list.user_id,
            f"Item '{todo_item.description}' in list '{todo_list.name}' set as completed",
        )

        # if all items are completed, mark the list as completed
        if all(i.status == TodoStatus.COMPLETED for i in todo_list.items):
            todo_list.status = TodoStatus.COMPLETED
            self.audit_repository.audit(
                AuditOperation.UPDATE, todo_list.user_id, f"List '{todo_list.name}' set as completed"
            )

        self.todo_repository.upsert_list(todo_list)  # updates list and items
        return todo_item
