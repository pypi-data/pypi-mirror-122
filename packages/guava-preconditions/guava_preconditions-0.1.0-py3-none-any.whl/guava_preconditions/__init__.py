from typing import TypeVar, Optional

T = TypeVar("T")


def checkArgument(expression: bool):
    "Ensures the truth of an expression involving one or more parameters to the calling method."
    pass


def checkArgument(expression: bool, errorMessage: Any):
    "Ensures the truth of an expression involving one or more parameters to the calling method."
    pass


def checkArgument(expression: bool, errorMessageTemplate: str, *errorMessageArgs: Any):
    "Ensures the truth of an expression involving one or more parameters to the calling method."
    pass


def checkElementIndex(index: int, size: int) -> int:
    "Ensures that index specifies a valid element in an array, list or string of size size."
    pass


def checkElementIndex(index: int, size: int, desc: str) -> int:
    "Ensures that index specifies a valid element in an array, list or string of size size."
    pass


def checkNotNull(reference: Optional[T]) -> T:
    "Ensures that an object reference passed as a parameter to the calling method is not null."
    pass


def checkNotNull(reference: Optional[T], errorMessage: Any) -> T:
    "Ensures that an object reference passed as a parameter to the calling method is not null."
    pass


def checkNotNull(
    reference: Optional[T], errorMessageTemplate: str, *errorMessageArgs: Any
) -> T:
    "Ensures that an object reference passed as a parameter to the calling method is not null."
    pass


def checkPositionIndex(index: int, size: int) -> int:
    "Ensures that index specifies a valid position in an array, list or string of size size."
    pass


def checkPositionIndex(index: int, size: int, desc: str) -> int:
    "Ensures that index specifies a valid position in an array, list or string of size size."
    pass


def checkPositionIndexes(start: int, end: int, size: int):
    "Ensures that start and end specify a valid positions in an array, list or string of size size, and are in order."
    pass


def checkState(expression: bool):
    "Ensures the truth of an expression involving the state of the calling instance, but not involving any parameters to the calling method."
    pass


def checkState(expression: bool, errorMessage: Any):
    "Ensures the truth of an expression involving the state of the calling instance, but not involving any parameters to the calling method."
    pass


def checkState(expression: bool, errorMessageTemplate: str, *errorMessageArgs: Any):
    "Ensures the truth of an expression involving the state of the calling instance, but not involving any parameters to the calling method."
    pass
