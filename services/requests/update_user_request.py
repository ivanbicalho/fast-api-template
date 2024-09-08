from dataclasses import dataclass


@dataclass
class UpdateUserRequest:
    id: int
    first_name: str
    last_name: str
    email: str
