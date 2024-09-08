from db.models import UserModel
from db.uow import UnitOfWork


class UserRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def get_user(self, user_id: int) -> UserModel | None:
        user_model = self.uow.session.query(UserModel).filter(UserModel.id == user_id).first()

        if user_model:
            return user_model

        return None

    def add(self, user: UserModel) -> UserModel:
        self.uow.session.add(user)
        self.uow.session.flush()
        return user

    def update(self, user: UserModel) -> UserModel:
        user_model = self.uow.session.query(UserModel).filter(UserModel.id == user.id).first()

        if not user_model:
            raise ValueError("User not found")

        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.email = user.email

        self.uow.session.add(user_model)
        self.uow.session.flush()
        return user_model
