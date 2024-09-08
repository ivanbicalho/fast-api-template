from dataclasses import dataclass


@dataclass
class AddUserRequest:
    first_name: str
    last_name: str
    email: str
