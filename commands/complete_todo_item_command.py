from db.enum import AuditOperation, TodoStatus
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository


class CompleteTodoItemCommand:
    def __init__(self, todo_repository: TodoRepository, audit_repository: AuditRepository) -> None:
        self.todo_repository = todo_repository
        self.audit_repository = audit_repository

    def run(self, todo_item_id: int) -> None:
        todo_list = self.todo_repository.get_list_from_item(todo_item_id)

        if not todo_list:
            raise ValueError(f"Item id {todo_item_id} not found")

        todo_item = next(i for i in todo_list.items if i.id == todo_item_id)
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

        self.todo_repository.upsert_list(todo_list)
