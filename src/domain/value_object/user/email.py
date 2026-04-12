import re

from src.domain.value_object.user.error.invalid_email_error import InvalidEmailError
from src.domain.value_object.value_object import ValueObject



class Email(ValueObject):
    _EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    @classmethod
    def _validate(cls, value: str):
        if not value:
            raise InvalidEmailError("Email cannot be empty")

        if value != value.strip():
            raise InvalidEmailError("Email cannot contain leading or trailing spaces")

        if not cls._EMAIL_REGEX.match(value):
            raise InvalidEmailError(f"Invalid email format: {value}")

        if len(value) > 254:
            raise InvalidEmailError("Email is too long")

        local_part, domain = value.split("@", 1)

        if len(local_part) > 64:
            raise InvalidEmailError("Local part too long")

        if len(domain) > 253:
            raise InvalidEmailError("Domain too long")
