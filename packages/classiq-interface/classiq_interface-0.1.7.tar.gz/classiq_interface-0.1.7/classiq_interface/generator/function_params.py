import abc
from enum import Enum
from typing import Optional, ClassVar, Type, Any

import pydantic


class DefaultInputEnum(Enum):
    pass


class DefaultOutputEnum(Enum):
    OUT = "OUT"


class IO(Enum):
    Input = "Input"
    Output = "Output"


class FunctionParams(pydantic.BaseModel, abc.ABC):
    _input_enum: Type[Enum] = pydantic.PrivateAttr(default=DefaultInputEnum)
    _output_enum: Type[Enum] = pydantic.PrivateAttr(default=DefaultOutputEnum)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.create_io_enums()

    def get_io_enum(self, io: IO) -> Type[Enum]:
        if io == IO.Input:
            return self._input_enum
        if io == IO.Output:
            return self._output_enum

    def create_io_enums(self):
        pass

    def is_valid_io_name(self, name: str, io: IO) -> bool:
        return name in self.get_io_enum(io).__members__
