from typing import cast
from db.models import UserModel
from domain.user import User
from db.uow import UnitOfWork
from services.requests.add_user_request import AddUserRequest
from services.requests.update_user_request import UpdateUserRequest


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def get_user(self, user_id: int) -> User | None:
        user_model = self.uow.session.query(UserModel).filter(UserModel.id == user_id).first()

        if user_model:
            return user_model

        return None

    def add(self, add_user_request: AddUserRequest) -> User:
        user_model = UserModel(
            first_name=add_user_request.first_name,
            last_name=add_user_request.last_name,
            email=add_user_request.email,
        )

        self.uow.session.add(user_model)
        self.uow.session.flush()
        return cast(User, user_model)

    def update(self, update_user_request: UpdateUserRequest) -> User:
        user_model = self.uow.session.query(UserModel).filter(UserModel.id == update_user_request.id).first()

        if not user_model:
            raise ValueError("User not found")

        user_model.first_name = update_user_request.first_name
        user_model.last_name = update_user_request.last_name
        user_model.email = update_user_request.email

        self.uow.session.add(user_model)
        self.uow.session.flush()
        return user_model
