from typing import Type


class WrongReturnType(Exception):
    def __init__(self, expected_type: Type, actual_type: Type):
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__()
