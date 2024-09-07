from fastapi import Depends
from services.todo_service import TodoService
from services.user_service import UserService
from db.uow import UnitOfWork


class Factory:
    @staticmethod
    def user_service(uow: UnitOfWork = Depends(UnitOfWork.new)) -> UserService:
        return UserService(uow)

    @staticmethod
    def todo_service(uow: UnitOfWork = Depends(UnitOfWork.new)) -> TodoService:
        return TodoService(uow)
