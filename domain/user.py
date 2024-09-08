from __future__ import annotations

from db.models import UserModel


class User(UserModel):
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


# @dataclass
# class User:
#     id: int
#     name: str
#     email: str

#     @staticmethod
#     def from_model(model: UserModel) -> User:
#         return User(
#             id=model.id,
#             name=model.name,
#             email=model.email,
#         )
