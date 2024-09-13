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

    def list_users(self) -> list[UserModel]:
        return self.uow.session.query(UserModel).all()

    def upsert(self, user: UserModel) -> UserModel:
        # if user.id:
        #     audit = AuditModel(operation="update", message=f"Updating user {user.id}")
        # else:
        #     audit = AuditModel(operation="insert", message=f"Adding new user {user.first_name}")

        # self.uow.session.add(audit)
        self.uow.session.add(user)
        self.uow.session.flush()
        return user
