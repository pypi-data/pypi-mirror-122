import abc
import ast
import datetime
import functools
import tarfile
from collections import OrderedDict
from typing import Iterable, Tuple, List, Union, Dict, Callable, Optional

import django.db.models
from django.db import models

import arrow
import graphene
import django_filters
import stringcase
from arrow import Arrow
from graphene import Scalar, Field
from graphene.types.unmountedtype import UnmountedType
from graphql.language import ast
from graphene_django import DjangoObjectType
from graphene_django_extras import LimitOffsetGraphqlPagination, DjangoInputObjectType, DjangoListObjectType

from django_koldar_utils.django_toolbox import django_helpers
from rest_framework import serializers

from django_koldar_utils.graphql_toolsbox.GraphQLHelper import GraphQLHelper
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneReturnType, TGrapheneQuery, TGrapheneMutation, \
    TGrapheneInputType, TGrapheneType, TDjangoModelType
from django_koldar_utils.graphql_toolsbox.scalars.ArrowDateScalar import ArrowDateScalar
from django_koldar_utils.graphql_toolsbox.scalars.ArrowDateTimeScalar import ArrowDateTimeScalar
from django_koldar_utils.graphql_toolsbox.scalars.ArrowDurationScalar import ArrowDurationScalar





# ##########################################################
# GRAPHENE CLASS
# ##########################################################


def create_graphene_tuple_input_type(name: str, it: Iterable[Tuple[str, TGrapheneInputType]]) -> TGrapheneInputType:
    """
    Programmatically create a type in graphene_toolbox repersenting a tuple of elements.

    :param name: name of the type
    :param it: an iteralbe of pairs, where the frist item is the field name repersenting the i-th element
        while the second item is the graphene_toolbox.FIeld type of said graphene_toolbox class field
    :return: type rerpesenting the tuple
    """
    properties = dict()
    for key, type in it:
        properties[key] = convert_field_into_input(graphene_field=type)
    result = type(
        name,
        (graphene.InputObjectType, ),
        properties
    )
    return result


def create_graphene_tuple_type(name: str, it: Iterable[Tuple[str, type]], description: str = None) -> type:
    """
    Programmatically create a type in graphene_toolbox repersenting a tuple of elements.

    :param name: name of the type
    :param description: optional description of this tuple
    :param it: an iteralbe of pairs, where the frist item is the field name repersenting the i-th element
        while the second item is the graphene_toolbox.FIeld type of said graphene_toolbox class field
    :return: type rerpesenting the tuple
    """
    l = list(it)

    if description is None:
        tuple_repr = '\n'.join(map(lambda pair: f" - {pair[0]} item is representing {pair[1][0]}", enumerate(l)))
        description = f"""Class that represents a tuple of size {len(l)} where: {tuple_repr}\n The tuple does not have further semantics."""

    properties = dict()
    for key, atype in l:
        if not isinstance(atype, graphene.Field):
            # fi the type is a scalar or a grapèhene type, we need to manually wrap it to Field.
            # in this way the type will appear in the _meta.fields as well
            atype = graphene.Field(atype)
        properties[key] = atype
    properties["__doc__"] = description

    result = type(
        name,
        (graphene.ObjectType, ),
        properties
    )
    return result


def create_graphene_pair_type(name: str, item0_name: str, item0_type: type, item1_name: str, item1_type: type) -> type:
    """
    Programmatically create a type in graphene_toolbox repersenting a pair of elements.

    :param name: name of the type
    :param item0_name: field name of the first item
    :param item0_type: field graphene_toolbox.FIeld type of the first item
    :param item1_name: field name of the second item
    :param item1_type: field graphene_toolbox.FIeld type of the second item
    :return: type rerpesenting the tuple
    """
    return create_graphene_tuple_type(name, [(item0_name, item0_type), (item1_name, item1_type)])


def create_graphql_class(cls, fields=None, specify_fields: Dict[str, Tuple[type, Optional[Callable[[any, any], any]]]]=None) -> type:
    """
    Create a graphQl type starting from a Django model

    :param cls: django_toolbox type of the model whose graphql_toolsbox type we want to generate
    :param fields: field that we wna tto include in the graphene_toolbox class type
    :param specify_fields: a dictionary of django_toolbox model fields which you want to personally customize.
        Each dictionary key is a django_toolbox model field name. Each value is a pair. If present, "fields" is ignored
         - first, mandatory, is the graphene_toolbox type that you want to use for the field
         - second, (optionally set to None) is a callable representing the resolver. If left missing we will just call
            the model field
    """

    def default_resolver(model_instance, info, field_name: str = None) -> any:
        return getattr(model_instance, field_name)

    if fields is None:
        fields = "__all__"
    if specify_fields is None:
        specify_fields = dict()

    meta_properties = {
        "model": cls,
        "description": cls.__doc__,
    }
    if len(specify_fields) > 0:
        meta_properties["exclude"] = list(specify_fields.keys())
    else:
        meta_properties["fields"] = fields
    graphql_type_meta = type(
        "Meta",
        (object, ),
        meta_properties
    )

    class_name = cls.__name__
    properties = {
        "Meta": graphql_type_meta,
    }
    # attach graphql_toolsbox type additional fields
    for field_name, value in specify_fields.items():
        if isinstance(value, tuple):
            graphene_type, resolver_function = value
        else:
            graphene_type = value
            resolver_function = None

        properties[field_name] = graphene_type
    for field_name, value in specify_fields.items():
        if isinstance(value, tuple):
            graphene_type, resolver_function = value
        else:
            graphene_type = value
            resolver_function = None

        if resolver_function is None:
            resolver_function = functools.partial(default_resolver, field_name=field_name)
        properties[f"resolve_{field_name}"] = resolver_function

    graphql_type = type(
        f"{class_name}GraphQLType",
        (DjangoObjectType, ),
        properties
    )

    return graphql_type


def create_graphql_list_type(cls) -> type:
    """
    A graphql_toolsbox type representing a list of a given class.
    This is used to generate list of DjancoObjectType
    See https://github.com/eamigo86/graphene-django-extras
    """
    graphql_type_meta = type(
        "Meta",
        (object, ),
        {
            "model": cls,
            "description": f"""GraphQL type representing a list of {cls.__name__}.""",
            "pagination": LimitOffsetGraphqlPagination(default_limit=25)
        }
    )

    class_name = cls.__name__
    graphql_type = type(
        f"{class_name}GraphQLListType",
        (DjangoListObjectType, ),
        {
            "Meta": graphql_type_meta
        }
    )
    return graphql_type

# ##########################################################
# GRAPHENE REGISTER
# ##########################################################


class GrapheneRegisterSlot(object):
    """
    A slot inside the register
    """

    __slots__ = ("atype", "graphene_type", "graphene_input_type", "django_field_type")

    def __init__(self, atype: type, graphene_type: TGrapheneReturnType, graphene_input_type: TGrapheneInputType, django_field_type: type):
        self.atype = atype
        self.graphene_type = graphene_type
        self.graphene_input_type = graphene_input_type
        self.django_field_type = django_field_type

    def _get_non_none(self, x, y, both_none) -> any:
        if x is None and y is not None:
            return y
        elif x is not None and y is None:
            return x
        elif x is None and y is None:
            return both_none
        elif x is not None and y is not None and y == x:
            return x
        else:
            raise ValueError(f"Different values {x} and {y} mismatch for slot {self}!")

    def merge(self, other: "GrapheneRegisterSlot") -> "GrapheneRegisterSlot":
        result = GrapheneRegisterSlot(self.atype, self.graphene_type, self.graphene_input_type, self.django_field_type, self.label)
        result.atype = self._get_non_none(self.atype, other.atype, None)
        result.graphene_type = self._get_non_none(self.graphene_type, other.graphene_type, None)
        result.graphene_input_type = self._get_non_none(self.graphene_input_type, other.graphene_input_type, None)
        result.django_field_type = self._get_non_none(self.django_field_type, other.django_field_type, None)
        result.label = self._get_non_none(self.label, other.label, None)

        return result


class GrapheneRegister(object):
    """
    An object that allows you to fetch all the graphene a nd graphene input types for a specific
    type. The type does not need to be a django model. Can be anything.
    """

    def __init__(self):
        self._registry_find_by_type: Dict[type, OrderedDict[any, GrapheneRegisterSlot]] = dict()
        """
        key are types. the values is dictioanry indexed by label value. The inner dictionary is an OrderedDict
        becuase we assume that the first label registered is the most important (or default one)
        
        We trade memory to improve the query timinfg when fetching graphene types and inputs types for a specific type  
        """
        self._registry_by_graphene_type: Dict[TGrapheneType, OrderedDict[any, GrapheneRegisterSlot]] = dict()
        """
        key are graphene types. the values are dictionaries indexed by label value. The inner dictionary is 
        an OrderedDict
        becuase we assume that the first label registered is the most important (or default one)
        
        We trade memory to improve the query timing when fetching types and inputs types for a specific graphene type  
        """
        self._registry_by_graphene_input: Dict[type, OrderedDict[any, GrapheneRegisterSlot]] = dict()
        """
        key are graphene input types. the values are dictionaries indexed by label value. The inner dictionary is an 
        OrderedDict
        becuase we assume that the first label registered is the most important (or default one)

        We trade memory to improve the query timing when fetching types and inputs types for a specific graphene 
        input type  
        """

    def register_base_types(self, label: str):
        """
        Automatically adds some graphene types and inputs for some base scenarios

        :param label: label to assign o every type
        """

        # TODO djang_field is not used at the moment
        label = stringcase.snakecase(label)

        # primitive
        self.register_mapping(
            atype=str,
            graphene_type=graphene.String,
            graphene_input_type=graphene.String,
            django_field=str,
            label_from_type=label, label_from_graphene=label, label_from_graphene_input=label,
        )
        self.register_mapping(
            atype=int,
            graphene_type=graphene.Int,
            graphene_input_type=graphene.Int,
            django_field=int,
            label_from_type=label, label_from_graphene=label, label_from_graphene_input=label,
        )
        self.register_mapping(
            atype=float,
            graphene_type=graphene.Float,
            graphene_input_type=graphene.Float,
            django_field=float,
            label_from_type=label, label_from_graphene=label, label_from_graphene_input=label,
        )
        self.register_mapping(
            atype=bool,
            graphene_type=graphene.Boolean,
            graphene_input_type=graphene.Boolean,
            django_field=bool,
            label_from_type=label, label_from_graphene=label, label_from_graphene_input=label,
        )

        # id
        self.register_mapping(
            atype=int,
            graphene_type=graphene.ID,
            graphene_input_type=graphene.ID,
            django_field=int,
            label_from_type=f"{label}_id",
            label_from_graphene=f"{label}_id",
            label_from_graphene_input=f"{label}_id",
        )

        # datetimes
        self.register_mapping(
            atype=arrow.Arrow,
            graphene_type=graphene.DateTime,
            graphene_input_type=ArrowDateTimeScalar,
            django_field=int,
            label_from_type=f"{label}_arrow",
            label_from_graphene=f"{label}_arrow",
            label_from_graphene_input=f"{label}_arrow",
        )
        self.register_mapping(
            atype=datetime.datetime,
            graphene_type=graphene.DateTime,
            graphene_input_type=graphene.DateTime,
            django_field=int,
            label_from_type=f"{label}_legacy",
            label_from_graphene=f"{label}_legacy",
            label_from_graphene_input=f"{label}_legacy",
        )

        #dates
        self.register_mapping(
            atype=datetime.date,
            graphene_type=graphene.Date,
            graphene_input_type=graphene.Date,
            django_field=int,
            label_from_type=f"{label}_legacy",
            label_from_graphene=f"{label}_legacy",
            label_from_graphene_input=f"{label}_legacy",
        )
        self.register_mapping(
            atype=arrow.Arrow,
            graphene_type=graphene.Date,
            graphene_input_type=ArrowDateScalar,
            django_field=int,
            label_from_type=f"{label}_arrow",
            label_from_graphene=f"{label}_arrow",
            label_from_graphene_input=f"{label}_arrow",
        )

        #durations
        self.register_mapping(
            atype=datetime.timedelta,
            graphene_type=graphene.Int,
            graphene_input_type=ArrowDurationScalar,
            django_field=int,
            label_from_type=f"{label}_arrow",
            label_from_graphene=f"{label}_arrow",
            label_from_graphene_input=f"{label}_arrow",
        )

        # base64
        self.register_mapping(
            atype=str,
            graphene_type=graphene.Base64,
            graphene_input_type=graphene.Base64,
            django_field=int,
            label_from_type=f"{label}",
            label_from_graphene=f"{label}",
            label_from_graphene_input=f"{label}",
        )

        # duration

        # if graphene_field_type._meta.name == "String":
        #     v = graphene.String(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Int":
        #     v = graphene.Int(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Boolean":
        #     v = graphene.Boolean(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ID":
        #     v = graphene.ID(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "DateTime":
        #     v = graphene.DateTime(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Date":
        #     v = graphene.Date(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ArrowDateTimeScalar":
        #     v = ArrowDateTimeScalar(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ArrowDateScalar":
        #     v = ArrowDateScalar(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ArrowDurationScalar":
        #     v = ArrowDurationScalar(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Base64":
        #     v = graphene.Base64(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Float":
        #     v = graphene.Float(required=False, default_value=t.default_value, description=t.description, **t.args)

    def register_mapping(self, atype: type, graphene_type: TGrapheneType, graphene_input_type: TGrapheneInputType, django_field: type, label_from_type: any, label_from_graphene: any, label_from_graphene_input: any):
        self._add_representation(t=atype,
                                 graphene_type=graphene_type,
                                 graphene_input=graphene_input_type,
                                 django_field=django_field,
                                 label_from_type=label_from_type,
                                 label_from_graphene=label_from_graphene,
                                 label_from_graphene_input=label_from_graphene_input,
                                )

    def _add_representation(self, t: type, graphene_type: TGrapheneType, graphene_input: Optional[TGrapheneInputType], django_field: type, label_from_type: any, label_from_graphene: any, label_from_graphene_input: any):
        new_slot = GrapheneRegisterSlot(atype=t, graphene_type=graphene_type, graphene_input_type=graphene_input, django_field_type=django_field)
        # _registry_find_by_type
        if t not in self._registry_find_by_type:
            self._registry_find_by_type[t] = OrderedDict()
        if label_from_type in self._registry_find_by_type[t]:
            # we try to merge
            present = self._registry_find_by_type[t][label_from_type]
            copy_slot = present.merge(new_slot)
        else:
            copy_slot = new_slot
        self._registry_find_by_type[t][label_from_type] = copy_slot

        # _registry_by_graphene_type
        if graphene_type not in self._registry_by_graphene_type:
            self._registry_by_graphene_type[graphene_type] = OrderedDict()
        if label_from_graphene in self._registry_by_graphene_type[graphene_type]:
            present = self._registry_by_graphene_type[graphene_type][label_from_graphene]
            copy_slot = present.merge(new_slot)
        else:
            copy_slot = new_slot
        self._registry_by_graphene_type[graphene_type][label_from_graphene] = copy_slot

        # _registry_by_graphene_input
        if graphene_input not in self._registry_by_graphene_input:
            self._registry_by_graphene_input[graphene_input] = OrderedDict()
        if label_from_graphene_input in self._registry_by_graphene_input[graphene_input]:
            present = self._registry_by_graphene_input[graphene_input][label_from_graphene_input]
            copy_slot = present.merge(new_slot)
        else:
            copy_slot = new_slot
        self._registry_by_graphene_input[graphene_input][label_from_graphene_input] = copy_slot

    def list_available_labels_for(self, atype: Union[type, TGrapheneType, TGrapheneInputType], target: str) -> Iterable[any]:
        if target == "type":
            yield from self._registry_find_by_type[atype].keys()
        elif target == "graphene":
            yield from self._registry_by_graphene_type[atype].keys()
        elif target == "input":
            yield from self._registry_by_graphene_input[atype].keys()
        else:
            raise ValueError(f"invalid target {target}")

    def list_available_labels_for_type(self, atype: type) -> Iterable[any]:
        return self.list_available_labels_for(atype, "type")

    def list_available_labels_for_graphene_type(self, atype: type) -> Iterable[any]:
        return self.list_available_labels_for(atype, "graphene")

    def list_available_labels_for_graphene_input_type(self, atype: type) -> Iterable[any]:
        return self.list_available_labels_for(atype, "input")

    def get_main_graphene_type_from_type(self, atype: type) -> TGrapheneType:
        return self._get_from(atype, generate="graphene", from_source="type")

    def get_main_graphene_input_type_from_type(self, atype: type, label: str = None) -> TGrapheneType:
        return self._get_from(atype, generate="input", from_source="type")

    def get_main_type_from_graphene_type(self, atype: TGrapheneType) -> TGrapheneType:
        return self._get_from(atype, generate="type", from_source="graphene")

    def get_main_graphene_input_type_from_graphene_type(self, atype: TGrapheneType) -> TGrapheneType:
        return self._get_from(atype, generate="input", from_source="graphene")

    def get_main_type_from_graphene_input_type(self, atype: TGrapheneType) -> TGrapheneType:
        return self._get_from(atype, generate="type", from_source="input")

    def get_main_graphene_type_from_graphene_input_type(self, atype: TGrapheneType) -> TGrapheneType:
        return self._get_from(atype, generate="graphene", from_source="input")


    def get_graphene_type_from_type(self, atype: type, label: str) -> TGrapheneType:
        return self._get_from(atype, generate="graphene", from_source="type", label=label)

    def get_graphene_input_type_from_type(self, atype: type, label: str) -> TGrapheneType:
        return self._get_from(atype, generate="input", from_source="type", label=label)

    def get_type_from_graphene_type(self, atype: TGrapheneType, label: str) -> TGrapheneType:
        return self._get_from(atype, generate="type", from_source="graphene", label=label)

    def get_graphene_input_type_from_graphene_type(self, atype: TGrapheneType, label: str) -> TGrapheneType:
        return self._get_from(atype, generate="input", from_source="graphene", label=label)

    def get_type_from_graphene_input_type(self, atype: TGrapheneType, label: str) -> TGrapheneType:
        return self._get_from(atype, generate="type", from_source="input", label=label)

    def get_graphene_input_type_from_graphene_input_type(self, atype: TGrapheneType, label: str) -> TGrapheneType:
        return self._get_from(atype, generate="graphene", from_source="input", label=label)

    def _get_from(self, atype: Union[type, TGrapheneType, TGrapheneInputType], generate: str, from_source: str, label: str = None) -> Union[TGrapheneType, TGrapheneInputType]:
        """
        Fetch the default implementation of the input for a given type

        :param atype: type whose input we need to retrieve
        :param from_source: the registry where to ftch data, either "type", "graphene" or "input"
        :param generate: the type to generate. either "type", "graphene" or "input"
        :param label: label rerpesenting the specific association you want to fetch. If None we pick the default one
        :return: an input representing the type
        :raise ValueError: if the type has no known input repersentation
        """
        if from_source == "type":
            if atype not in self._registry_find_by_type:
                raise ValueError(f"Cannot find type that represents the type {atype.__name__}!")
            label_dict = self._registry_find_by_type[atype]
        elif from_source == "graphene":
            if atype not in self._registry_by_graphene_type:
                raise ValueError(f"Cannot find type that represents the graphene type {atype.__name__}!")
            label_dict = self._registry_by_graphene_type[atype]
        elif from_source == "input":
            if atype not in self._registry_by_graphene_input:
                raise ValueError(f"Cannot find type that represents the graphene input type {atype.__name__}!")
            label_dict = self._registry_find_by_type[atype]
        else:
            raise ValueError(f"from_source needs to be either type, graphene or input, not {from_source}!")

        if len(label_dict) == 0:
            raise ValueError(f"there is an error in the registry! There are no slots for type {atype.__name__}!")
        elif len(label_dict) == 1:
            slot = next(iter(label_dict.values()))
        else:
            if label is None:
                # the user has specified no labels. We exploit the OrderDict to get the first slot, which
                # is by definition the default one
                slot = next(iter(label_dict.values()))
            else:
                # fetch the slot requested by the user
                slot = label_dict[label]

        if generate == "type":
            return slot.atype
        elif generate == "graphene":
            return slot.graphene_type
        elif generate == "input":
            return slot.graphene_input_type
        else:
            raise ValueError(f"invalid kind. Either type, graphene or input are accepted, not {generate}!")


class AbstractGrapheneInputGenerator(abc.ABC):
    """
    An object that allows you to generate inputs starting from types
    """

    @abc.abstractmethod
    def _convert_field_into_input(self, field_name: str,
                                graphene_field: TGrapheneReturnType,
                                graphene_field_original: TGrapheneReturnType,
                                graphene_type: TGrapheneType,
                                register: GrapheneRegister,
                                  ) -> TGrapheneReturnType:
        """
        Convert a graphene type (or a field from the django_toolbox model) into a type that can be used in a input.

        :param register:  register to fetch input of complex object whose input
            is not straightforward to compute
        :param graphene_field: the field to convert. Thsi value has been preprocessed to specify only the important bit
            of the type
        :param graphene_field_original: the field to convert. Fetched from graphene_type
        :param graphene_type: if graphene_field is None, we convert the association graphene_toolbox field belonging to the django_toolbox model model_field
            (e.g., BigInteger into ID)
        :param field_specifier: if graphene_field is None, we need something tha tspecify what it the field in graphene_type
            that we want to convert. May be:
             - the field name in the graphene_toolbox type to convert;
             - the graphene_toolbox field instance;
             - the django_toolbox model field instance (we assume there is the same name);
        """
        pass

        # # query the register and fetch the association graphene input
        # graphene_input_type = register.get_main_graphene_input_type_from_graphene_type(graphene_field)
        # result = graphene_input_type(
        #     required=False,
        #     default_value=graphene_field_original.default_value,
        #     description=graphene_field_original.description,
        #     **graphene_field_original.args
        # )
        # return result

        # # if the type is a Field, fetch encapsuled type
        # if isinstance(t, graphene.Field):
        #     # a field may have "of_type" or "_type" inside it  conaining the actual field to convert
        #     if hasattr(t.type, "of_type"):
        #         graphene_field_type = t.type.of_type
        #     else:
        #         # this represents a complex graphql_toolsbox object (e.g. AuthorGraphQL). We need to convert it into an input
        #         raise NotImplementedError()
        # else:
        #     graphene_field_type = t.type
        #
        # # we need to fetch the corresponding field and strap away the possible "required" field. The rest can remain the same
        # if graphene_field_type._meta.name == "String":
        #     v = graphene.String(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Int":
        #     v = graphene.Int(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Boolean":
        #     v = graphene.Boolean(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ID":
        #     v = graphene.ID(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "DateTime":
        #     v = graphene.DateTime(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Date":
        #     v = graphene.Date(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ArrowDateTimeScalar":
        #     v = ArrowDateTimeScalar(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ArrowDateScalar":
        #     v = ArrowDateScalar(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "ArrowDurationScalar":
        #     v = ArrowDurationScalar(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Base64":
        #     v = graphene.Base64(required=False, default_value=t.default_value, description=t.description, **t.args)
        # elif graphene_field_type._meta.name == "Float":
        #     v = graphene.Float(required=False, default_value=t.default_value, description=t.description, **t.args)
        # else:
        #     raise ValueError(f"cannot handle type {t} (name = {graphene_field_type._meta.name})!")
        #
        # return v

    @abc.abstractmethod
    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        """
        Check if you should include the field in the input to generate

        :param field_name: name of the field to consider
        :param field_type: pre-processed type of field_name. If possible, use this: it is much easier to handle
        :param original_field_type: original type of the field_name
        :return: treu if this field should be considered, false otherwise
        """
        pass

    def _get_field(self, t: Union[TGrapheneType], name: str) -> TGrapheneReturnType:
        """
        :param t: the entity owning the field
        :param name: name of the field to fetch
        :raise KeyError: if we cannot find the field in the type
        :return: graphene type isntance representing the field
        """
        result = getattr(t, name)
        result = GraphQLHelper.get_actual_type_from_field(result)
        return result

    def create_graphql_input_type(self, graphene_type: TGrapheneType, class_name: str, field_names: Iterable[str],
                            description: str = None,
                            register: GrapheneRegister = None,
                              ) -> type:
        """
        Create an input class from a **django_toolbox model** specifying only primitive types.
        All such types are optional (not required)

        :param graphene_type: graphene type that we will use to create the assoicated graphene_toolbox input type
        :param class_name: name of the input class to create
        :param field_names: field names of the graphene_toolbox type (or maybe the associated django_toolbox type) that we will use to create the input
        :param description: descritpion of the input class. None to put a defualt one
            If returns none, we will no include the "model" field in the meta input class
        :param register: a structure that maps types and fetch their corresponding graphene and input types
        :return: input class
        """

        # class PersonInput(graphene.InputObjectType):
        #     name = graphene.String(required=True)
        #     age = graphene.Int(required=True)

        if description is None:
            description = f"""The graphene input type associated to the type {class_name}. See {class_name} for further information"""

        input_fields = {}
        for field_name in field_names:
            try:
                graphene_field_original = getattr(graphene_type, field_name)
                field = self.get_field(graphene_type, field_name)
            except KeyError:
                # we could not find the field
                continue
            if not self.should_you_include_field(field_name, field, graphene_field_original):
                continue
            v = self._convert_field_into_input(
                field_name=field_name,
                graphene_field_original=graphene_field_original,
                graphene_field=field,
                graphene_type=graphene_type,
                register=register,
            )
            input_fields[field_name] = v

        properties = dict()
        properties["description"] = description
        properties["__doc__"] = description
        properties.update(input_fields)

        input_graphql_type = type(
            class_name,
            (graphene.InputObjectType,),
            properties
        )

        return input_graphql_type

    # def generate_primitive_input(self, django_type: TDjangoModelType, graphene_type: TGrapheneType, exclude_fields: List[str] = None) -> TGrapheneInputType:
    #     """
    #     Create an input class from a **django model** specifying only primitive types.
    #     The fields of the django type will become all optional (not required)
    #     """
    #
    #     if exclude_fields is None:
    #         exclude_fields = []
    #
    #     def generate_input_field(field_name: str, f: any, graphene_type: TGrapheneType) -> any:
    #         v = self._convert_field_into_input(
    #             graphene_type=graphene_type,
    #             field_specifier=f,
    #         )
    #         return v
    #
    #     def should_be_exluded(field_name: str, f: any) -> bool:
    #         nonlocal exclude_fields
    #         return field_name in exclude_fields
    #
    #     class_name = django_type.__name__
    #     result = self._create_graphql_input(
    #         class_name=f"{stringcase.pascalcase(class_name)}PrimitiveGraphQLInput",
    #         graphene_type=graphene_type,
    #         fields=django_helpers.get_primitive_fields(django_type),
    #         description=f"""The graphql_toolsbox input tyep associated to the type {class_name}. See {class_name} for further information""",
    #         generate_input_field=generate_input_field,
    #         should_be_excluded=should_be_exluded,
    #     )
    #
    #     return result


class MakeAllFieldsAsOptionalMixIn:

    def _convert_field_into_input(self, field_name: str,
                                  graphene_field: TGrapheneReturnType,
                                  graphene_field_original: TGrapheneReturnType,
                                  graphene_type: TGrapheneType,
                                  register: GrapheneRegister,
                                  ) -> TGrapheneReturnType:
        # query the register and fetch the association graphene input
        graphene_input_type = register.get_main_graphene_input_type_from_graphene_type(graphene_field)
        result = graphene_input_type(
            required=False,
            default_value=graphene_field_original.default_value,
            description=graphene_field_original.description,
            **graphene_field_original.args
        )
        return result


class ExcludePrimaryKeyMixIn:
    """
    MixIn to add to a AbstractGrapheneInputGenerator implementation
    exclude any field that is a primary key (type ID)
    """

    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        return GraphQLHelper.is_field_id(field_type)


class ExcludeNonPrimitiveFieldMixIn:
    """
        MixIn to add to a AbstractGrapheneInputGenerator implementation
        Include everything!
        """

    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        return GraphQLHelper.is_field_non_primitive(original_field_type)


class IncludeEveryFieldMixIn:
    """
    MixIn to add to a AbstractGrapheneInputGenerator implementation
    Include everything!
    """

    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType,
                                  original_field_type: TGrapheneReturnType) -> bool:
        return True


class ExcludeSecretsMixIn:
    """
    MixIn to add to a AbstractGrapheneInputGenerator implementation
    Exclude all password related fields
    """

    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        for x in ["password", "psw", "secret", "forget_token"]:
            if x in field_name:
                return False
        return True


class ExcludeActiveMixIn:
    """
    MixIn to add to a AbstractGrapheneInputGenerator implementation
    Exclude all field containign "active" word
    """

    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        for x in ["active", ]:
            if x in field_name:
                return False
        return True


class ExcludeActiveAndSecrets:
    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        return all(map(lambda cls: super(cls, self)._should_you_include_field(field_name, field_type, original_field_type), [ExcludeActiveMixIn, ExcludeSecretsMixIn, ]))


class ExcludeActiveNonPrimitiveAndSecrets:
    def _should_you_include_field(self, field_name: str, field_type: TGrapheneReturnType, original_field_type: TGrapheneReturnType) -> bool:
        return all(map(lambda cls: super(cls, self)._should_you_include_field(field_name, field_type, original_field_type), [ExcludeActiveMixIn, ExcludeSecretsMixIn, ExcludeNonPrimitiveFieldMixIn]))


class StandardInputGenerator(MakeAllFieldsAsOptionalMixIn, ExcludeActiveAndSecrets, AbstractGrapheneInputGenerator):
    """
    Inputs containing all fields in the graphene type, except active and sensitive ones. All fields are marked as optional
    """
    pass


class PrimitiveInputGenerator(MakeAllFieldsAsOptionalMixIn, ExcludeActiveNonPrimitiveAndSecrets, AbstractGrapheneInputGenerator):
    """
    Input containign only primitive fields, except active and sensitive ones. All fields are marked as optional
    """
    pass


DEFAULT_REGISTER: GrapheneRegister = GrapheneRegister()
DEFAULT_REGISTER.register_base_types("default")
DEFAULT_GRAPHENE_INPUT_GENERATOR: AbstractGrapheneInputGenerator = StandardInputGenerator()
DEFAULT_GRAPHENE_PRIMITIVE_INPUT_GENERATOR: AbstractGrapheneInputGenerator = PrimitiveInputGenerator()


def create_graphql_primitive_input(django_type: type, graphene_type: type, exclude_fields: List[str] = None) -> type:
    """
    Create an input class from a **django_toolbox model** specifying only primitive types.
    All such types are optional (not required)
    """

    if exclude_fields is None:
        exclude_fields = []

    # def generate_input_field(field_name: str, f: any, graphene_type: TGrapheneType) -> any:
    #     v = convert_field_into_input(
    #         graphene_type=graphene_type,
    #         field_specifier=f,
    #     )
    #     return v
    #
    # def should_be_exluded(field_name: str, f: any) -> bool:
    #     nonlocal exclude_fields
    #     return field_name in exclude_fields

    class_name = django_type.__name__
    field_names = list(map(lambda x: x.name, filter(lambda x: x.name in exclude_fields, django_helpers.get_primitive_fields(django_type))))

    result = DEFAULT_GRAPHENE_PRIMITIVE_INPUT_GENERATOR.create_graphql_input_type(
        graphene_type=graphene_type,
        class_name=f"{stringcase.pascalcase(class_name)}PrimitiveGraphQLInput",
        field_names=field_names,
        description=f"""The graphql_toolsbox input tyep associated to the type {class_name}. See {class_name} for further information""",
        register=DEFAULT_REGISTER,
    )
    return result

    # class_name = django_type.__name__
    # result = _create_graphql_input(
    #     class_name=f"{stringcase.pascalcase(class_name)}PrimitiveGraphQLInput",
    #     graphene_type=graphene_type,
    #     fields=django_helpers.get_primitive_fields(django_type),
    #     description=f"""The graphql_toolsbox input tyep associated to the type {class_name}. See {class_name} for further information""",
    #     generate_input_field=generate_input_field,
    #     should_be_excluded=should_be_exluded,
    # )
    #
    # return result


def create_graphql_input(cls) -> type:
    """
    Create a graphene input by calling django extra package.
    Note that this will not include the id. You may need it or not.
    See dujango extras
    """

    graphql_type_meta = type(
        "Meta",
        (object, ),
        {
            "model": cls,
            "description": f"""
                Input type of class {cls.__name__}.
            """
        }
    )

    class_name = cls.__name__
    graphql_type = type(
        f"{class_name}GraphQLInput",
        (DjangoInputObjectType, ),
        {
            "Meta": graphql_type_meta
        }
    )

    return graphql_type


def create_graphene_tuple_input(name: str, it: Iterable[Tuple[str, TGrapheneInputType]], description: str = None) -> TGrapheneInputType:
    """
    Programmatically create a type in graphene_toolbox repersenting an input tuple of elements.

    :param name: name of the type
    :param description: optional description of this tuple
    :param it: an iteralbe of pairs, where the frist item is the field name repersenting the i-th element
        while the second item is the graphene_toolbox.FIeld type of said graphene_toolbox class field
    :return: graphene_toolbox input type rerpesenting the tuple
    """
    l = list(it)

    if description is None:
        tuple_repr = '\n'.join(map(lambda pair: f" - {pair[0]} item is representing {pair[1][0]}", enumerate(l)))
        description = f"""Class that represents a tuple of size {len(l)} where: {tuple_repr}\n The tuple does not have further semantics."""

    properties = dict()
    for key, atype in l:
        if not isinstance(atype, graphene.Field):
            # fi the type is a scalar or a grapèhene type, we need to manually wrap it to Field.
            # in this way the type will appear in the _meta.fields as well
            # we mark the field as non required, since this is an input
            atype = graphene.Field(atype, required=False)
        properties[key] = atype
    properties["__doc__"] = description

    result = type(
        name,
        (graphene.InputObjectType, ),
        properties
    )
    return result


# ################################################################
# SERIALIZERS
# ################################################################



def create_serializer(cls) -> type:
    """
    A serializer allowing to easily create mutations
    See https://github.com/eamigo86/graphene-django-extras
    """
    graphql_type_meta = type(
        "Meta",
        (object, ),
        {
            "model": cls,
        }
    )

    class_name = cls.__name__
    graphql_type = type(
        f"{class_name}Serializer",
        (serializers.ModelSerializer, ),
        {
            "Meta": graphql_type_meta
        }
    )
    return graphql_type