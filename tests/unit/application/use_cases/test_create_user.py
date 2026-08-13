import pytest

from src.application.use_cases.create_user import CreateUserUseCase
from src.domain.value_object.user.email import Email
from src.domain.value_object.user.password import Password

from src.application.exceptions.user_exceptions import UserAlreadyExistsError

class FakeUserRepository:
    def __init__(self, user_exists=False, add_error=None):
        self.user_exists = user_exists
        self.added_user = None
        self.add_error = add_error

    async def exists_by_email(self, email):
        return self.user_exists

    async def add(self, user):
        if self.add_error:
            raise self.add_error

        self.added_user = user


class StubPasswordHasher:
    def hash(self, password):
        return "hashed-password"

class FakeUnitOfWork:
    def __init__(self, users):
        self.users = users
        self.exited = False
        self.exit_exception_type = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exited = True
        self.exit_exception_type = exc_type


class FakeUnitOfWorkFactory:
    def __init__(self, uow):
        self.uow = uow

    def __call__(self):
        return self.uow


@pytest.mark.asyncio
async def test_create_user_saves_user_with_hashed_password():
    # Arrange
    repository = FakeUserRepository()
    hasher = StubPasswordHasher()

    uow = FakeUnitOfWork(repository)
    uow_factory = FakeUnitOfWorkFactory(uow)

    use_case = CreateUserUseCase(
        uow_factory=uow_factory,
        hasher=hasher,
    )

    email = Email("test@example.com")
    password = Password("Password123!")

    # Act
    await use_case(
        email=email,
        password=password,
        name="John",
        surname="Doe",
    )

    assert repository.added_user is not None

    assert repository.added_user.email == email
    assert repository.added_user.name == "John"
    assert repository.added_user.surname == "Doe"

    assert repository.added_user.hashed_password == "hashed-password"

    assert uow.exited is True


@pytest.mark.asyncio
async def test_create_user_raises_when_email_already_exists():
    # Arrange
    repository = FakeUserRepository(user_exists=True)
    hasher = StubPasswordHasher()
    uow = FakeUnitOfWork(repository)
    uow_factory = FakeUnitOfWorkFactory(uow)

    use_case = CreateUserUseCase(
        hasher=hasher,
        uow_factory=uow_factory,
    )
    email = Email("test@example.com")
    password = Password("Password123!")

    with pytest.raises(UserAlreadyExistsError):
         await use_case(
                email=email,
                password=password,
                name="John",
                surname="Doe",
            )
    assert repository.added_user is None
    assert uow.exited is True


@pytest.mark.asyncio
async def test_create_user_propagates_repository_error():
    repository = FakeUserRepository(
        add_error=RuntimeError("save failed")
    )

    hasher = StubPasswordHasher()
    uow = FakeUnitOfWork(repository)
    uow_factory = FakeUnitOfWorkFactory(uow)

    use_case = CreateUserUseCase(
        hasher=hasher,
        uow_factory=uow_factory,
    )
    email = Email("test@example.com")
    password = Password("Password123!")

    # Act
    with pytest.raises(RuntimeError, match="save failed"):
        await use_case(
            email=email,
            password=password,
            name="John",
            surname="Doe",
        )

    # Assert
    assert repository.added_user is None
    assert uow.exited is True
    assert uow.exit_exception_type is RuntimeError
