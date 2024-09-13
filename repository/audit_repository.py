from enum import Enum
from db.enum import AuditOperation
from db.models import AuditModel
from db.uow import UnitOfWork


class AuditRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def audit(self, operation: AuditOperation, message: str) -> None:
        audit = AuditModel(operation=operation, message=message)
        self.uow.session.add(audit)
        self.uow.session.flush()
