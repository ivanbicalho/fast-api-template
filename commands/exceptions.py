class UserNotFound(Exception):
    def __init__(self, user_id: int):
        self.message = f"User with id {user_id} not found"
        super().__init__(self.message)


class TodoListNotFound(Exception):
    def __init__(self, list_id: int):
        self.message = f"Todo list with id {list_id} not found"
        super().__init__(self.message)


class TodoItemNotFound(Exception):
    def __init__(self, item_id: int):
        self.message = f"Todo item with id {item_id} not found"
        super().__init__(self.message)
