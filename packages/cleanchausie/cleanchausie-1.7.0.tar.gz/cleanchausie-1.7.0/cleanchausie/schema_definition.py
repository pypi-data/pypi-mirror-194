import itertools
import typing
from typing import Any, Callable, Dict, Generic, TypeVar, Union

import attr

from cleanchausie.consts import empty, omitted
from cleanchausie.errors import Errors, ValidationError
from cleanchausie.fields.field import Field
from cleanchausie.fields.validation import Value, validate_field
from cleanchausie.utils import getter

T = TypeVar("T")


@attr.frozen
class SchemaDefinition(Generic[T]):
    fields: Dict[str, Field]
    factory: Callable[..., T]


def clean(
    schema_definition: SchemaDefinition[T], data: Any, context: Any = empty
) -> Union[T, ValidationError]:
    """Entrypoint for cleaning some set of data for a given schema definition."""
    field_defs = [
        (name, f_def) for name, f_def in schema_definition.fields.items()
    ]

    # fake an initial 'self' result so function-defined fields can
    # optionally include an unused "self" parameter
    results: Dict[str, Union[Value, Errors]] = {"self": Value(value=None)}

    # initial set are those with met deps
    eval_queue: typing.List[typing.Tuple[str, Field]] = []
    delayed_eval = []
    for name, f in field_defs:
        if not f.depends_on or all([d in results for d in f.depends_on]):
            eval_queue.append((name, f))
        else:
            delayed_eval.append((name, f))
    assert len(field_defs) == len(eval_queue) + len(delayed_eval)

    while eval_queue:
        field_name, field_def = eval_queue.pop()

        if field_def.accepts is not None:
            accepts = field_def.accepts or (field_name,)
            value: Any = empty
            for accept in accepts:
                value = getter(data, accept, omitted)
                if value is not omitted:
                    break
            assert value is not empty
        else:
            value = empty

        results[field_name] = validate_field(
            field=field_def,
            path=(field_name,),
            root_value=data,
            value=value,
            context=context,
            intermediate_results=results,
        )

        queued_fields = {n for n, _f in eval_queue}
        for name, f in delayed_eval:
            if (
                name not in results
                and name not in queued_fields
                and all(
                    [
                        (dep in results and isinstance(results[dep], Value))
                        for dep in f.depends_on
                    ]
                )
            ):
                eval_queue.append((name, f))

    errors = list(
        itertools.chain(
            *[
                v.flatten()
                for v in results.values()
                if not isinstance(v, Value)
            ]
        )
    )
    if errors:
        return ValidationError(errors=errors)

    # we already checked for errors above, but this extra explicit check
    # helps mypy figure out what's going on.
    validated_values = {
        k: v.value
        for k, v in results.items()
        if isinstance(v, Value) and k != "self"
    }
    assert set(validated_values.keys()) == {f_name for f_name, _ in field_defs}
    return schema_definition.factory(**validated_values)


def serialize(
    schema_definition: SchemaDefinition, data: Dict[str, Any]
) -> Dict:
    """Serialize a schema to a dictionary, respecting serialization settings."""
    result = {
        (field_def.serialize_to or field_name): (
            field_def.serialize_func(data[field_name])
            if data[field_name] is not None
            else None
        )
        for field_name, field_def in schema_definition.fields.items()
        if data.get(field_name, omitted) is not omitted
    }
    return {k: v for k, v in result.items() if v is not omitted}


def make_clean_with_factory(
    schema_def: SchemaDefinition, factory: Callable[..., T]
) -> Callable[[Any, Any], Union[ValidationError, T]]:
    """Make a function that cleans then calls `factory` with cleaned data."""
    new_def = attr.evolve(schema_def, factory=factory)

    def _schema_def_cleaner(
        data: Any, context: Any = empty
    ) -> Union[ValidationError, T]:
        return clean(new_def, data, context)

    return _schema_def_cleaner
