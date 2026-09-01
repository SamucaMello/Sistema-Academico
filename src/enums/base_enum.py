
from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def to_list(cls) -> list:
        return list(cls)


