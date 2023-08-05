from typing import Any, Optional


class DeepError(Exception):
    def __init__(self, message: str) -> None:
        Exception.__init__(self, message)


def error(message: str) -> DeepError:
    return DeepError(message)


def check_created(element: Any, description: str) -> Any:
    if not element:
        raise error(f"Failed to create {description}")
    return element
