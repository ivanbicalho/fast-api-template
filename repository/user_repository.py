from db.models import User
from db.uow import UnitOfWork


class UserRepository:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def get_user(self, user_id: int) -> User | None:
        return self._uow.session.query(User).filter(User.id == user_id).first()

    def list_users(self) -> list[User]:
        return self._uow.session.query(User).all()

    def upsert(self, user: User) -> User:
        self._uow.session.add(user)
        self._uow.session.flush()
        return user
