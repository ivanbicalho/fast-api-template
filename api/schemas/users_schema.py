from __future__ import annotations
from pydantic import BaseModel

from domain.user import User
from services.requests.add_user_request import AddUserRequest


class InitRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    default_list_name: str

    def to_add_user_request(self) -> AddUserRequest:
        return AddUserRequest(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Ivan",
                "last_name": "Bicalho",
                "email": "ivanribeirob@gmail.com",
                "default_list_name": "My first list",
            }
        }


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Ivan",
                "last_name": "Bicalho",
                "email": "ivanribeirob@gmail.com",
            }
        }


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    @staticmethod
    def from_user(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
