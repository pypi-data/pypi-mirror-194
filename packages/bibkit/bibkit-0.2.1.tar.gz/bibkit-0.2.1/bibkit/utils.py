from typing import NamedTuple, Union
from enum import Enum


class ValidationFailure(Enum):
    """
    Validation failure types
    """

    WRONG_TYPE = 1
    WRONG_FORMAT = 2
    WRONG_CHECK_DIGIT = 3


ValidationResult = NamedTuple(
    "ValidationResult",
    [("is_valid", bool), ("failure_reason", Union[ValidationFailure, None])],
)
"""
Utility tuple for validation results

:param bool is_valid: Whether the validation was successful or not
:param failure_reason: Reason for the failure
:type failure_reason: Optional[str]
"""
