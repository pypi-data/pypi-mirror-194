from __future__ import annotations

import contextlib
import enum
from functools import cached_property
from typing import Any, Optional, Type

from attrs import define

from qtgql.codegen.py.compiler.builtin_scalars import BuiltinScalar
from qtgql.codegen.py.runtime.bases import QGraphQListModel
from qtgql.codegen.py.runtime.custom_scalars import BaseCustomScalar, CustomScalarMap
from qtgql.codegen.utils import AntiForwardRef
from qtgql.utils.typingref import TypeHinter


class Kinds(enum.Enum):
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    ENUM = "ENUM"
    LIST = "LIST"
    UNION = "UNION"
    NON_NULL = "NON_NULL"
    INTERFACE = "INTERFACE"
    INPUT_OBJECT = "INPUT_OBJECT"


@define(slots=False)
class GqlFieldDefinition:
    name: str
    type: GqlTypeHinter
    type_map: dict[str, GqlTypeDefinition]
    enums: EnumMap
    scalars: CustomScalarMap
    description: Optional[str] = ""

    @cached_property
    def default_value(self):
        if builtin_scalar := self.type.is_builtin_scalar:
            if builtin_scalar.tp is str:
                return f"'{builtin_scalar.default_value}'"
            return f"{builtin_scalar.default_value}"
        if self.type.is_object_type:
            return "None"

        if self.type.is_model:
            # this would just generate the model without data.
            return "list()"

        if custom_scalar := self.type.is_custom_scalar(self.scalars):
            return f"SCALARS.{custom_scalar.__name__}()"

        if enum_def := self.type.is_enum:
            return f"{enum_def.name}(1)"  # 1 is where auto() starts.

        return "None"  # Unions are not supported yet.

    @property
    def is_custom_scalar(self) -> Optional[Type[BaseCustomScalar]]:
        return self.type.is_custom_scalar(self.scalars)

    @cached_property
    def annotation(self) -> str:
        """
        :returns: Annotation of the field based on the real type,
        meaning that the private attribute would be of that type.
        this goes for init and the property setter.
        """
        return self.type.annotation(self.scalars)

    @cached_property
    def fget_annotation(self) -> str:
        """This annotates the value that is QML-compatible."""
        if custom_scalar := self.type.is_custom_scalar(self.scalars):
            return TypeHinter.from_annotations(
                custom_scalar.to_qt.__annotations__["return"]
            ).stringify()
        if self.type.is_enum:
            return "int"

        return self.annotation

    @cached_property
    def property_type(self) -> str:
        try:
            # this should raise if it is an inner type.
            ret = GqlTypeHinter.from_string(self.fget_annotation, self.type_map)
            if ret.type in self.type_map.values():
                raise TypeError  # in py3.11 the get_type_hints won't raise so raise brutally
            return self.fget_annotation
        except (TypeError, NameError):
            if self.type.is_union():
                # graphql doesn't support scalars in Unions ATM. (what about Enums in unions)?
                return "QObject"
            if self.type.is_enum:
                # QEnum value must be int
                return "int"
            # might be a model, which is also QObject
            assert self.type.is_model or self.type.is_object_type
            return "QObject"

    @cached_property
    def setter_name(self) -> str:
        return self.name + "_setter"

    @cached_property
    def signal_name(self) -> str:
        return self.name + "Changed"

    @cached_property
    def private_name(self) -> str:
        return "_" + self.name

    @property
    def fget(self) -> str:
        if self.type.is_custom_scalar(self.scalars):
            return f"return self.{self.private_name}.{BaseCustomScalar.to_qt.__name__}()"
        if self.type.is_enum:
            return f"return self.{self.private_name}.value"
        return f"return self.{self.private_name}"


@define(slots=False)
class GqlTypeDefinition:
    name: str
    fields_dict: dict[str, GqlFieldDefinition]
    docstring: Optional[str] = ""

    @property
    def fields(self) -> list[GqlFieldDefinition]:
        return list(self.fields_dict.values())


@define
class EnumValue:
    """encapsulates enumValues from introspection, maps to an Enum member."""

    name: str
    description: str = ""


@define
class GqlEnumDefinition:
    name: str
    members: list[EnumValue]


EnumMap = dict[str, "GqlEnumDefinition"]


class GqlTypeHinter(TypeHinter):
    def __init__(
        self,
        type: Any,
        of_type: tuple[GqlTypeHinter, ...] = (),
    ):
        self.type = type
        self.of_type: tuple[GqlTypeHinter, ...] = of_type

    @property
    def is_object_type(self) -> Optional[GqlTypeDefinition]:
        with contextlib.suppress(TypeError):
            if issubclass(self.type, AntiForwardRef):
                ret = self.type.resolve()
                if isinstance(ret, GqlTypeDefinition):
                    return ret

    @property
    def is_model(self) -> Optional[GqlTypeDefinition]:
        if self.is_list():
            # enums and scalars are not supported in lists yet (valid graphql spec though)
            return self.of_type[0].is_object_type

    @property
    def is_enum(self) -> Optional[GqlEnumDefinition]:
        with contextlib.suppress(TypeError):
            if issubclass(self.type, AntiForwardRef):
                if isinstance(self.type.resolve(), GqlEnumDefinition):
                    return self.type.resolve()

    @property
    def is_builtin_scalar(self) -> Optional[BuiltinScalar]:
        if isinstance(self.type, BuiltinScalar):
            return self.type

    def is_custom_scalar(self, scalars: CustomScalarMap) -> Optional[Type[BaseCustomScalar]]:
        if self.type in scalars.values():
            return self.type

    def annotation(self, scalars: CustomScalarMap) -> str:
        """
        :returns: Annotation of the field based on the real type,
        meaning that the private attribute would be of that type.
        this goes for init and the property setter.
        """
        # int, str, float etc...
        if builtin_scalar := self.is_builtin_scalar:
            return builtin_scalar.tp.__name__

        if scalar := self.is_custom_scalar(scalars):
            return f"SCALARS.{scalar.__name__}"
        if gql_enum := self.is_enum:
            return gql_enum.name
        # handle Optional, Union, List etc...
        # removing redundant prefixes.
        if model_of := self.is_model:
            return f"{QGraphQListModel.__name__}[{model_of.name}]"
        if object_def := self.is_object_type:
            return f"Optional[{object_def.name}]"
        if self.is_union():
            return "Union[" + ",".join(th.annotation(scalars) for th in self.of_type) + "]"
        raise NotImplementedError  # pragma no cover

    def as_annotation(self, object_map=None):  # pragma: no cover
        raise NotImplementedError("not safe to call on this type")
