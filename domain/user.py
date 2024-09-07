from __future__ import annotations
from dataclasses import dataclass

from db.models import UserModel


@dataclass
class User:
    id: int
    name: str
    email: str

    @staticmethod
    def from_model(model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
        )
