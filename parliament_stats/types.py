"""
Custom type to render stats columns
"""
from collections import OrderedDict

from graphene import Field
from graphene.types.interface import Interface
from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.types import construct_fields, get_global_registry

class ColumnClubStatsType(ObjectType):

    @classmethod
    def __init_subclass_with_meta__(
                                    cls,
                                    interfaces=(),
                                    possible_types=(),
                                    default_resolver=None,
                                    _meta=None,
                                    model=None,
                                    only_fields=(),
                                    exclude_fields=(),
                                    **options
    ):

        if not _meta:
            _meta = ObjectTypeOptions(cls)

        registry = get_global_registry()
        django_fields = yank_fields_from_attrs(
            construct_fields(model, registry, only_fields, exclude_fields), _as=Field
        )

        assert not (possible_types and cls.is_type_of), (
            "{name}.Meta.possible_types will cause type collision with {name}.is_type_of. "
            "Please use one or other."
        ).format(name=cls.__name__)

        _meta.fields = django_fields

        _meta.interfaces = interfaces
        _meta.possible_types = possible_types
        _meta.default_resolver = default_resolver
        super().__init_subclass_with_meta__(_meta=_meta, **options)
