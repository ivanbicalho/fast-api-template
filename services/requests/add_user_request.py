from dataclasses import dataclass


@dataclass
class AddUserRequest:
    name: str
    email: str
