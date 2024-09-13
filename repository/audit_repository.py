from enum import Enum
from db.enum import AuditOperation
from db.models import Audit
from db.uow import UnitOfWork


class AuditRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def audit(self, operation: AuditOperation, user_id: int, message: str) -> None:
        audit = Audit(operation=operation, user_id=user_id, message=message)
        self._uow.session.add(audit)
        self._uow.session.flush()
