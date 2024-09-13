from __future__ import annotations
from pydantic import BaseModel
from db.models import UserModel
from use_cases.add_user_use_case import AddUserUseCaseRequest


class UserRequest(BaseModel):
    name: str
    email: str
    default_list_name: str

    def to_service_request(self) -> AddUserUseCaseRequest:
        # We made it better in the /v2/users
        name_parts = self.name.split(" ")
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        return AddUserUseCaseRequest(
            first_name=first_name,
            last_name=last_name,
            email=self.email,
            default_list_name=self.default_list_name,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ivan Bicalho",
                "email": "ivanribeirob@gmail.com",
                "default_list_name": "My first list",
            }
        }


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    @staticmethod
    def from_user(user: UserModel) -> UserResponse:
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
