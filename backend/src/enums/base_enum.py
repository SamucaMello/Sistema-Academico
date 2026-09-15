
from enum import Enum


class AppBaseEnum(Enum):
    @classmethod
    def to_list(cls) -> list:
        return list(cls)


