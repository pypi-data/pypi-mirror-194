from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from cleanchausie.consts import empty
from cleanchausie.errors import Errors, ValidationError
from cleanchausie.fields.field import Field, field

if TYPE_CHECKING:
    from cleanchausie.schema import Schema

NestedFieldType = TypeVar("NestedFieldType", bound="Schema")


def NestedField(  # noqa: N802
    inner_schema: Type[NestedFieldType],
) -> Field[NestedFieldType]:
    def _call(
        value: Any, context: Any = empty
    ) -> Union[NestedFieldType, Errors]:
        result = inner_schema.clean(value, context=context)
        if isinstance(result, ValidationError):
            return Errors(errors=result.errors)
        elif isinstance(result, inner_schema):
            return result

        raise TypeError

    def _serialize_fn(value: NestedFieldType) -> Dict:
        return value.serialize()

    return field(_call, serialize_func=_serialize_fn)
