import re

from src.domain.value_object.user.error.invalid_password_error import InvalidPasswordError
from src.domain.value_object.value_object import ValueObject


class Password(ValueObject):
    @classmethod
    def _validate(cls, value: str):
        errors = []

        if len(value) < 8:
            errors.append("The password must be at least 8 characters long")

        if not re.search(r"[A-Z]", value):
            errors.append("The password must contain a capital letter: A-Z")

        if not re.search(r"[a-z]", value):
            errors.append("The password must contain a lowercase letter: a-z")

        if not re.search(r"\d", value):
            errors.append("The password must contain a number: 0-9")

        if not re.search(r"[!@#$%^&*()]", value):
            errors.append("The password must contain a special character: !@#$%^&*()")

        if errors:
            raise InvalidPasswordError(".\n".join(errors))