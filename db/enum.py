from enum import Enum


class TodoStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class AuditOperation(Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
