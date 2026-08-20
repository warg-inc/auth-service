from typing import Optional

from src.domain.value_object.user.email import Email
from src.domain.value_object.user.password import Password


class User:
    def __init__(self, email: Email, surname: str, name: str, hashed_password: str, id: Optional[int] = None):
        if not email:
            raise ValueError("email cannot be empty")
        if not surname:
            raise ValueError("surname cannot be empty")
        if not name:
            raise ValueError("name cannot be empty")
        if not hashed_password:
            raise ValueError("password_hashed cannot be empty")

        self.email = email
        self.name = name
        self.surname = surname
        self.hashed_password = hashed_password
        self.id = id
