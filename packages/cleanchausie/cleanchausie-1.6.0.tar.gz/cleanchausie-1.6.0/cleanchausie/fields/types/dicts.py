from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional as T_Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from cleanchausie.consts import empty
from cleanchausie.errors import Error, Errors
from cleanchausie.fields.field import Field
from cleanchausie.fields.validation import UnvalidatedMappedValue, Value

DictKeyType = TypeVar("DictKeyType")
DictValueType = TypeVar("DictValueType")


class DictField(Generic[DictKeyType, DictValueType]):
    key_field: T_Optional[Field[DictKeyType]]
    value_field: T_Optional[Field[DictValueType]]

    def __init__(
        self,
        key_field: T_Optional[Field[DictKeyType]],
        value_field: T_Optional[Field[DictValueType]],
    ) -> None:
        self.key_field = key_field
        self.value_field = value_field

    def __call__(
        self, value: Any, context: Any = empty
    ) -> Union[
        UnvalidatedMappedValue[DictKeyType, DictValueType], Error, Errors
    ]:
        if not isinstance(value, dict):
            return Error("Value is not a dictionary")
        return UnvalidatedMappedValue(
            value=value,
            # these casts directly line up with the value on the type, which
            # mypy reads incorrectly for some reason.
            key_field=cast(T_Optional[Field[DictKeyType]], self.key_field),
            value_field=cast(
                T_Optional[Field[DictValueType]], self.value_field
            ),
            construct=self.construct,
        )

    @staticmethod
    def construct(
        mapped_pairs: List[Tuple[Value, Value]]
    ) -> Dict[DictKeyType, DictValueType]:
        return {k.value: v.value for k, v in mapped_pairs}
