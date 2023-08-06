import abc
from typing import List

from ya_fattura_elettronica_generator import models


class ValidationOutcome(object):

    def __init__(self, kind: str, message: str):
        """

        :param kind: warning or error or ok
        :param message: mesage to output
        """
        self.kind = kind
        self.message = message

    @property
    def is_warning(self) -> bool:
        return self.kind == "warning"

    @property
    def is_error(self) -> bool:
        return self.kind == "error"

    @property
    def is_ok(self) -> bool:
        return self.kind == "ok"

    @classmethod
    def ok(cls, message: str) -> "ValidationOutcome":
        return ValidationOutcome("ok", message)

    @classmethod
    def warning(cls, message: str) -> "ValidationOutcome":
        return ValidationOutcome("warning", message)

    @classmethod
    def error(cls, message: str) -> "ValidationOutcome":
        return ValidationOutcome("error", message)


class IFatturaElettronicaValidator(abc.ABC):
    """
    An object that check if a fattura elettronica object is compliant against some criterion
    """

    @abc.abstractmethod
    def validate(self, fattura_elettronica: models.FatturaElettronicaType, context) -> List[ValidationOutcome]:
        """
        Perform a sequence of checks to ensure that the fattura elettronica is for sure compliant
        :param context:
        :return: list of errors the fattura has
        """
        pass

    def print_validation_summary(self, outcome: List[ValidationOutcome]):
        errors = 0
        print("ERRORS:")
        for i, x in enumerate(filter(lambda x: x.is_error, outcome)):
            errors += 1
            print(f" {i:02d}. {x.message}")
        print("")
        warnings = 0
        print("WARNINGS:")
        for i, x in enumerate(filter(lambda x: x.is_warning, outcome)):
            warnings += 1
            print(f" {i:02d}. {x.message}")
        print("")
        print("SUCCESSES:")
        for i, x in enumerate(filter(lambda x: x.is_ok, outcome)):
            print(f" {i:02d}. {x.message}")

        print(f"Validation has determined that fattura has {errors} errors and {warnings} warnings!")



