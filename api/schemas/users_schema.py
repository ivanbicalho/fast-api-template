from __future__ import annotations
from pydantic import BaseModel

from domain.user import User
from services.requests.add_user_request import AddUserRequest


class InitRequest(BaseModel):
    name: str
    email: str
    default_list_name: str

    def to_add_user_request(self) -> AddUserRequest:
        return AddUserRequest(
            name=self.name,
            email=self.email,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ivan Bicalho",
                "email": "ivanribeirob@gmail.com",
                "default_list_name": "My first list",
            }
        }


class UserRequest(BaseModel):
    name: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Ivan Bicalho",
                "email": "ivanribeirob@gmail.com",
            }
        }


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    @staticmethod
    def from_user(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
        )
