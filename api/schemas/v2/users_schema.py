from __future__ import annotations
from pydantic import BaseModel
from db.models import User
from commands.add_user_command import AddUserCommandRequest


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    default_list_name: str

    def to_service_request(self) -> AddUserCommandRequest:
        return AddUserCommandRequest(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            default_list_name=self.default_list_name,
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
