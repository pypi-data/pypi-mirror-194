from typing import Callable


def boolean(value: str) -> bool:
    return value.lower() in ("1", "true", "yes", "on", "y", "t")


def items(separatror: str = ",") -> Callable[[str], list[str]]:
    def _list(value: str) -> list[str]:
        return value.split(separatror)

    return _list


comma_separated = items()
