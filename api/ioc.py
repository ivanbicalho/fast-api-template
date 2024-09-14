from __future__ import annotations
from typing import Any, Generator
from fastapi import Depends
from commands.add_todo_item_command import AddTodoItemCommand
from commands.add_todo_list_command import AddTodoListCommand
from commands.complete_todo_item_command import CompleteTodoItemCommand
from repository.audit_repository import AuditRepository
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository
from db.uow import UnitOfWork
from commands.add_user_command import AddUserCommand


# This is exclusive for FastAPI
# -----------------------------
# FastAPI handles dependencies in a very nice way, and we can use it to create a simple IoC container
# This module is responsible for creating the dependencies that will be used in the routes


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


def audit_repository(uow: UnitOfWork = Depends(uow)) -> AuditRepository:
    return AuditRepository(uow)


def add_user_command(
    user_repository: UserRepository = Depends(user_repository),
    todo_repository: TodoRepository = Depends(todo_repository),
    audit_repository: AuditRepository = Depends(audit_repository),
) -> AddUserCommand:
    return AddUserCommand(user_repository, todo_repository, audit_repository)


def add_todo_list_command(
    user_repository: UserRepository = Depends(user_repository),
    todo_repository: TodoRepository = Depends(todo_repository),
    audit_repository: AuditRepository = Depends(audit_repository),
) -> AddTodoListCommand:
    return AddTodoListCommand(user_repository, todo_repository, audit_repository)


def add_todo_item_command(
    todo_repository: TodoRepository = Depends(todo_repository),
    audit_repository: AuditRepository = Depends(audit_repository),
) -> AddTodoItemCommand:
    return AddTodoItemCommand(todo_repository, audit_repository)


def complete_todo_item_command(
    todo_repository: TodoRepository = Depends(todo_repository),
    audit_repository: AuditRepository = Depends(audit_repository),
) -> CompleteTodoItemCommand:
    return CompleteTodoItemCommand(todo_repository, audit_repository)
