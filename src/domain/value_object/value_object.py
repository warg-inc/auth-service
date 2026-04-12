from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ValueObject:
    value: str

    def __post_init__(self):
        self._validate(self.value)

    @classmethod
    def _validate(cls, value: str):
        raise NotImplementedError
