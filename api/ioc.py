from __future__ import annotations
from typing import Any, Generator
from fastapi import Depends
from services.todo_service import TodoService
from services.user_service import UserService
from db.uow import UnitOfWork


def uow() -> Generator[UnitOfWork, Any, None]:
    # FastAPI supports dependencies that do some extra steps after finishing
    # To do this, we can use yield instead of return, and write the extra steps after
    # For UnitOfWork, we want to commit/rollback the transaction and close the session after finishing
    # During a request, the same UnitOfWork instance will be used in all dependencies that depend on it
    # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    with UnitOfWork() as uow:
        yield uow


class IoC:
    @staticmethod
    def user_service(uow: UnitOfWork = Depends(uow)) -> UserService:
        return UserService(uow)

    @staticmethod
    def todo_service(uow: UnitOfWork = Depends(uow)) -> TodoService:
        return TodoService(uow)
