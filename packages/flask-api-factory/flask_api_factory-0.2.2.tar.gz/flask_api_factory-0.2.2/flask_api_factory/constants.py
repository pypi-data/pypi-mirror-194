from enum import Enum


class ResourceTypes(int, Enum):
    RETRIVE = 1
    LIST = 2
    CREATE = 4
    UPDATE = 8
    PARTIAL_UPDATE = 16
    DESTROY = 32

    READ_ONLY = RETRIVE | LIST
    ALL = RETRIVE | LIST | CREATE | UPDATE | PARTIAL_UPDATE | DESTROY
