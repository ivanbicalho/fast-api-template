from __future__ import annotations
from types import TracebackType
from typing import Type
from db.database import default_session_factory

# Unit of Work
# Maintains a list of objects affected by a business transaction and coordinates
# the writing out of changes and the resolution of concurrency problems.
# https://martinfowler.com/eaaCatalog/unitOfWork.html


class UnitOfWork:
    def __init__(self) -> None:
        self._session_factory = default_session_factory

    def __enter__(self) -> UnitOfWork:
        self.session = self._session_factory()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
