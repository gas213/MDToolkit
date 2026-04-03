from enum import Enum
from typing import Type, TypeVar

T = TypeVar("T", bound=Enum)

class CommandValidationHelper:
    def __init__(self, command_name: str):
        self._command_name = command_name

    def parse_float(self, arg: str) -> float:
        try:
            return float(arg)
        except ValueError:
            raise Exception(f"{self._command_name} command: expected float instead of '{arg}'")
        
    def parse_float_or_none(self, arg: str) -> float | None:
        if arg.lower() == "none":
            return None
        else:
            return self.parse_float(arg)

    def parse_int(self, arg: str) -> int:
        try:
            return int(arg)
        except ValueError:
            raise Exception(f"{self._command_name} command: expected integer instead of '{arg}'")
        
    def check_for_exact_arg_count(self, args: list[str], expected_arg_count: int):
        if len(args) != expected_arg_count:
            raise Exception(f"{self._command_name} command does not have the right number of args (expected {expected_arg_count}, got {len(args)})")

    def check_for_min_arg_count(self, args: list[str], min_arg_count: int):
        if len(args) < min_arg_count:
            raise Exception(f"{self._command_name} command does not have enough args (expected at least {min_arg_count}, got {len(args)})")

    def check_categorical_arg(self, arg_value: str, enum_class: Type[T]) -> T:
        if not any(arg_value == item.value for item in enum_class):
            raise Exception(f"Unsupported {self._command_name} argument value specified in configuration: '{arg_value}' (supported values are {[item.value for item in enum_class]})")
        return enum_class(arg_value)