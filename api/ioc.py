from __future__ import annotations
from typing import Any, Generator
from fastapi import Depends
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository
from db.uow import UnitOfWork
from use_cases.add_user_use_case import AddUserUseCase


def uow() -> Generator[UnitOfWork, Any, None]:
    # FastAPI supports dependencies that do some extra steps after finishing
    # To do this, we can use yield instead of return, and write the extra steps after
    # For UnitOfWork, we want to commit/rollback the transaction and close the session after finishing
    # During a request, the same UnitOfWork instance will be used in all dependencies that depend on it
    # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    with UnitOfWork() as uow:
        yield uow


def user_repository(uow: UnitOfWork = Depends(uow)) -> UserRepository:
    return UserRepository(uow)


def todo_repository(uow: UnitOfWork = Depends(uow)) -> TodoRepository:
    return TodoRepository(uow)


def add_user_use_case(
    user_repository: UserRepository = Depends(user_repository),
    todo_repository: TodoRepository = Depends(todo_repository),
) -> AddUserUseCase:
    return AddUserUseCase(user_repository, todo_repository)
