from __future__ import annotations
from typing import Any, Generator
from db.database import default_session_factory


class UnitOfWork:
    def __init__(self) -> None:
        self._session_factory = default_session_factory

    def __enter__(self) -> UnitOfWork:
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    @staticmethod
    def new() -> Generator[UnitOfWork, Any, None]:
        with UnitOfWork() as uow:
            yield uow
