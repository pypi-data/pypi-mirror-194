"""
Base functionality
"""

# Copyright 2018-2020 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from functools import wraps
from collections import defaultdict
from datetime import datetime, date
import warnings
from copy import copy
from io import BytesIO
import logging
from uuid import UUID
import mimetypes

from six import with_metaclass
from requests.exceptions import HTTPError
import requests
try:
    from tabulate import tabulate
    have_tabulate = True
except ImportError:
    have_tabulate = False
try:
    from pyxus.resources.entity import Instance
    have_pyxus = True
except ImportError:
    have_pyxus = False
from .errors import ResolutionFailure
from .utility import (compact_uri, expand_uri, standard_context, namespace_from_id, as_list,
                      ATTACHMENT_SIZE_LIMIT)
from .registry import Registry, generate_cache_key, lookup, lookup_by_id, lookup_type, lookup_by_iri


logger = logging.getLogger("fairgraph")
mimetypes.init()


#class KGObject(object, metaclass=Registry):
class KGObject(with_metaclass(Registry, object)):
    """Base class for Knowledge Graph objects"""
    object_cache = {}
    save_cache = defaultdict(dict)
    query_id = "fgSimple"
    query_id_resolved = "fgResolved"
    fields = []
    existence_query_fields = ["name"]
    # Note that this default value of existence_query_fields should in
    # many cases be over-ridden.
    # It assumes that "name" is unique within instances of a given type,
    # which may often not be the case.

    def __init__(self, id=None, instance=None, **properties):
        if not have_pyxus:
            raise ImportError("Support for KG version 2 requires the pyxus package.")
        if self.fields:
            for field in self.fields:
                try:
                    value = properties[field.name]
                except KeyError:
                    if field.required:
                        raise ValueError("Field '{}' is required.".format(field.name))
                    value = None
                if value is None:
                    value = field.default
                    if callable(value):
                        value = value()
                elif IRI in field.types:
                    value = IRI(value)
                elif isinstance(value, (list, tuple)) and len(value) == 0:  # empty list
                    value = None
                field.check_value(value)
                setattr(self, field.name, value)
        else:
            for key, value in properties.items():
                if key not in self.property_names:
                    errmsg = "{name} got an unexpected keyword argument '{key}'"
                    raise TypeError(errmsg.format(name=self.__class__.__name__, key=key))
                else:
                    setattr(self, key, value)

        self.id = id
        self.instance = instance

    def __repr__(self):
        if self.fields:
            template_parts = ("{}={{self.{}!r}}".format(field.name, field.name)
                              for field in self.fields if getattr(self, field.name) is not None)
            template = "{self.__class__.__name__}(" + ", ".join(template_parts) + ", id={self.id})"
            return template.format(self=self)
        else:  # temporary, while converting all classes to use fields
            return ('{self.__class__.__name__}('
                    '{self.name!r} {self.id!r})'.format(self=self))

    @classmethod
    def from_kg_instance(cls, instance, client, use_cache=True, resolved=False):
        if cls.fields:
            D = instance.data
            if resolved:
                D = cls._fix_keys(D)
            if "@type" in D and D["@type"]:
                for otype in as_list(cls.type):
                    if otype not in D["@type"]:
                        # todo: profile - move compaction outside loop?
                        compacted_types = compact_uri(D["@type"], standard_context)
                        if otype not in compacted_types:
                            print("Warning: type mismatch {} - {}".format(otype, compacted_types))
            else:
                print("Warning: type information not available")
            args = {}
            for field in cls.fields:
                if field.intrinsic:
                    data_item = D.get(field.path)
                    # todo: handle over-loaded fields, e.g. "used" in ValidationActivity
                else:
                    data_item = D["@id"]
                args[field.name] = field.deserialize(data_item, client, resolved=resolved)
            return cls(id=D["@id"], instance=instance, **args)
        else:
            raise NotImplementedError("To be implemented by child class")

    @classmethod
    def _fix_keys(cls, data):
        """
        The KG Query API does not allow the same field name to be used twice in a document.
        This is a problem when resolving linked nodes which use the same field names
        as the 'parent'. As a workaround, we prefix the field names in the linked node
        with the class name.
        This method removes this prefix.
        This feels like a kludge, and I'd be happy to find a better solution.
        """
        prefix = cls.__name__ + "__"
        for key in list(data):
            # need to use list() in previous line to avoid
            # "dictionary keys changed during iteration" error in Python 3.8+
            if key.startswith(prefix):
                fixed_key = key.replace(prefix, "")
                data[fixed_key] = data.pop(key)
        return data

    @classmethod
    def from_uri(cls, uri, client, use_cache=True, deprecated=False, api="query",
                 scope="released", resolved=False):
        instance = client.instance_from_full_uri(uri, cls=cls, use_cache=use_cache,
                                                 deprecated=deprecated, api=api, scope=scope,
                                                 resolved=resolved)
        if instance is None:
            return None
        else:
            try:
                return cls.from_kg_instance(instance, client, use_cache=use_cache, resolved=resolved)
            except ValueError as err:
                return None

    @classmethod
    def from_uuid(cls, uuid, client, deprecated=False, api="query",
                  scope="released", resolved=False):
        logger.info("Attempting to retrieve {} with uuid {}".format(cls.__name__, uuid))
        if len(uuid) == 0:
            raise ValueError("Empty UUID")
        try:
            val = UUID(uuid, version=4)  # check validity of uuid
        except ValueError as err:
            raise ValueError("{} - {}".format(err, uuid))
        uri = cls.uri_from_uuid(uuid, client)
        return cls.from_uri(uri, client, deprecated=deprecated, api=api,
                            scope=scope, resolved=resolved)

    @classmethod
    def from_id(cls, id, client, use_cache=True, deprecated=False, api="query",
                scope="released", resolved=False):
        if id.startswith("http"):
            return cls.from_uri(id, client, use_cache, deprecated, api, scope, resolved)
        else:
            return cls.from_uuid(id, client, deprecated, api, scope, resolved)

    @property
    def uuid(self):
        return self.id.split("/")[-1]

    @classmethod
    def uri_from_uuid(cls, uuid, client):
        return "{}/data/{}/{}".format(client.nexus_endpoint, cls.path, uuid)

    @classmethod
    def list(cls, client, size=100, from_index=0, api="query",
             scope="released", resolved=False, **filters):
        """List all objects of this type in the Knowledge Graph"""

        def get_filter_value(filters, field):
            value = filters[field.name]
            if not isinstance(value, field.types):
                if isinstance(value, str) and issubclass(field.types[0], OntologyTerm):
                    value = field.types[0](value)
                else:
                    raise TypeError("{} must be of type {}".format(field.name, field.types))
            if hasattr(value, "iri"):
                filter_value = value.iri
            elif hasattr(value, "id"):
                filter_value = value.id
            else:
                filter_value = value
            return filter_value

        if api == 'nexus':
            context = {
                'nsg': 'https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/',
                'prov': 'http://www.w3.org/ns/prov#',
                "schema": "http://schema.org/"
            }
            filter_queries = []
            if filters:
                for field in cls.fields:
                    if field.name in filters:
                        if field.path.startswith("http"):
                            path = field.path
                        else:
                            #"path": cls.context[field.path],  # todo: fix contexts
                            path = standard_context[field.path]
                        filter_queries.append({
                            "path": path,
                            "op": "eq",
                            "value": get_filter_value(filters, field)
                        })
            if len(filter_queries) == 0:
                filter_query = None
            elif len(filter_queries) == 1:
                filter_query = filter_queries[0]
            else:
                filter_query = {
                    "op": "and",
                    "value": filter_queries
                }
        else:  # api="query"
            filter_queries = {}
            if filters:
                for field in cls.fields:
                    if field.name in filters:
                        filter_queries[field.name] = get_filter_value(filters, field)
            filter_query = filter_queries or None
            context = None
        return client.list(cls, from_index=from_index, size=size, api=api, scope=scope,
                           resolved=resolved, filter=filter_query, context=context)

    @classmethod
    def count(cls, client, api="query", scope="released"):
        return client.count(cls, api=api, scope=scope)

    def _build_existence_query(self, api="query"):
        query_fields = []
        for field_name in self.existence_query_fields:
            for field in self.fields:
                if field.name == field_name:
                    query_fields.append(field)
                    break
        if len(query_fields) < 1:
            raise Exception("Empty existence query for class {}".format(self.__class__.__name__))
        if api in ("query", "any"):
            return {
                field.name: field.serialize(getattr(self, field.name), None, for_query=True)
                for field in query_fields
            }
        elif api == "nexus":
            query_parts = []
            for field in query_fields:
                if field.path.startswith("http"):
                    path = field.path
                else:
                    path = standard_context[field.path]
                query_parts.append({
                    "path": path,
                    "op": "eq",
                    "value": field.serialize(getattr(self, field.name), None, for_query=True)
                })
            if len(query_fields) == 1:
                return query_parts[0]
            else:
                return {
                    "op": "and",
                    "value": query_parts
                }
        else:
            raise ValueError("'api' must be either 'nexus' or 'query'")

    def exists(self, client, api="query"):
        """Check if this object already exists in the KnowledgeGraph"""
        if self.id:
            return True
        else:
            query_filter = self._build_existence_query(api=api)
            query_cache_key = generate_cache_key(query_filter)
            if query_cache_key in self.save_cache[self.__class__]:
                # Because the KnowledgeGraph is only eventually consistent, an instance
                # that has just been written to Nexus may not appear in the query.
                # Therefore we cache the query when creating an instance and
                # where exists() returns True
                self.id = self.save_cache[self.__class__][query_cache_key]
                return True
            elif api == "any":
                if self.exists(client, "nexus"):
                    return True
                else:
                    return self.exists(client, "query")
            elif api == "nexus":
                context = {"schema": "http://schema.org/",
                           "prov": "http://www.w3.org/ns/prov#",
                           "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"}
                response = client.query_nexus(self.__class__.path, query_filter, context)

            elif api == "query":
                response = client.query_kgquery(self.__class__.path, self.query_id, filter=query_filter,
                                                size=1, scope="latest")
                # not sure about the appropriate scope here
            else:
                raise ValueError("'api' must be 'nexus', 'query' or 'any'")
            if response:
                # self.instance = response[0]   - this is a problem if retrieved with query API as rev will be 0
                self.id = response[0].data["@id"]
                KGObject.save_cache[self.__class__][query_cache_key] = self.id
            return bool(response)

    def get_context(self, client=None):
        context_urls = set()
        if isinstance(self.context, dict):
            context_dict = self.context
        elif isinstance(self.context, (list, tuple)):
            context_dict = {}
            for item in self.context:
                if isinstance(item, dict):
                    context_dict.update(item)
                else:
                    assert isinstance(item, str)
                    if "{{base}}" in item:
                        if client:
                            context_urls.add(item.replace("{{base}}", client.nexus_endpoint))
                    else:
                        assert item.startswith("http")
                        context_urls.add(item)
        else:
            raise ValueError("Unexpected value for context")

        if self.instance:
            instance_context = self.instance.data.get("@context", {})
            if isinstance(instance_context, dict):
                context_dict.update(instance_context)
            elif isinstance(instance_context, str):
                context_urls.add(instance_context)
            else:
                assert isinstance(instance_context, (list, tuple))
                for item in instance_context:
                    if isinstance(item, dict):
                        context_dict.update(item)
                    else:
                        assert isinstance(item, str) and item.startswith("http")
                        context_urls.add(item)

        context = list(context_urls) + [context_dict]
        if len(context) == 1:
            context = context[0]
        return context

    def _update_needed(self, data):
        for key, value in data.items():
            if key not in self.instance.data:
                if value is not None:
                    logger.info(f"new field '{key}' with value {value}")  # todo: change to debug
                    return True
            elif self.instance.data[key] != value:
                existing = self.instance.data[key]
                if (
                    isinstance(existing, list)
                    and len(existing) == 1
                    and isinstance(existing[0], dict)
                    and existing[0] == value
                ): # we treat a list containing a single dict as equivalent to that dict
                    return False
                logger.info(f"change to field '{key}' from {existing} to {value}")
                return True
        return False

    def _build_data(self, client, all_fields=False):
        if self.fields:
            data = {}
            for field in self.fields:
                if field.intrinsic:
                    value = getattr(self, field.name)
                    if all_fields or field.required or value is not None:
                        serialized = field.serialize(value, client)
                        if field.path in data:
                            if isinstance(data[field.path], list):
                                data[field.path].append(serialized)
                            else:
                                data[field.path] = [data[field.path], serialized]
                        else:
                            data[field.path] = serialized
            return data
        else:
            raise NotImplementedError("to be implemented by child classes")

    def save(self, client):
        """docstring"""

        if self.id or self.exists(client, api="any"):
            # note that calling self.exists() sets self.id if the object does exist
            if self.instance is None:
                # this can occur if updating a previously-saved object that has been constructed
                # (e.g. in a script), rather than retrieved from Nexus
                # since we don't know its current revision, we have to retrieve it

                # we have to use the Nexus API to get the revision number
                self.instance = client.instance_from_full_uri(
                    self.id, cls=self.__class__, api="nexus", scope="latest", use_cache=False)

        if self.instance:
            data = self._build_data(client, all_fields=True)
            if self._update_needed(data):
                logger.info("Updating - {}(id={})".format(self.__class__.__name__, self.id))
                self.instance.data.update(data)
                self.instance.data["@context"] = self.get_context(client)
                if "@type" in self.instance.data:
                    instance_type = compact_uri(self.instance.data["@type"], standard_context)
                    assert set(instance_type) == set(self.type), "{} != {}".format(set(instance_type), set(self.type))
                self.instance = client.update_instance(self.instance)
            else:
                logger.info("Not updating {}(id={}), unchanged".format(self.__class__.__name__,
                                                                       self.id))
        else:
            data = self._build_data(client)
            logger.info("Creating instance with data {}".format(data))
            data["@context"] = self.get_context(client)
            data["@type"] = self.type
            instance = client.create_new_instance(self.__class__.path, data)
            self.id = instance.data["@id"]
            self.instance = instance
            existence_query = self._build_existence_query(api="nexus")
            # make the cache key api-independent?
            KGObject.save_cache[self.__class__][generate_cache_key(existence_query)] = self.id
        logger.debug("Updating cache for object {}. Current state: {}".format(self.id, self._build_data(client)))
        KGObject.object_cache[self.id] = self

    def delete(self, client):
        """Deprecate"""
        client.delete_instance(self.instance)
        if self.id in KGObject.object_cache:
            KGObject.object_cache.pop(self.id)

    @classmethod
    def by_name(cls, name, client, match="equals", all=False, api="query",
                scope="released", resolved=False):
        return client.by_name(cls, name, match=match, all=all, api=api,
                              scope="released", resolved=resolved)

    @property
    def rev(self):
        if self.instance:
            return self.instance.data.get("nxv:rev", None)
        else:
            return None

    def resolve(self, client, api="query", scope="released", use_cache=True, follow_links=0):
        """To avoid having to check if a child attribute is a proxy or a real object,
        a real object resolves to itself.
        """
        if follow_links > 0:
            for field in self.fields:
                if issubclass(field.types[0], KGObject):
                    values = getattr(self, field.name)
                    resolved_values = []
                    for value in as_list(values):
                        if isinstance(value, (KGProxy, KGQuery)):
                            try:
                                resolved_value = value.resolve(
                                    client, api=api, scope=scope, use_cache=use_cache,
                                    follow_links=follow_links - 1)
                            except ResolutionFailure as err:
                                warnings.warn(str(err))
                                resolved_values.append(value)
                            else:
                                resolved_values.append(resolved_value)
                        elif isinstance(value, KGObject):  # already resolved
                            resolved_values.append(value)
                    if isinstance(values, (KGProxy, KGObject)):
                        assert len(resolved_values) == 1
                        resolved_values = resolved_values[0]
                    elif values is None:
                        assert len(resolved_values) == 0
                        resolved_values = None
                    setattr(self, field.name, resolved_values)
        return self

    @classmethod
    def set_strict_mode(cls, value, field_name=None):
        if value not in (True, False):
            raise ValueError("value should be either True or False")
        if field_name:
            for field in cls.fields:
                if field.name == field_name:
                    field.strict_mode = value
                    return
            raise ValueError("No such field: {}".format(field_name))
        else:
            for field in cls.fields:
                field.strict_mode = value

    def show(self, max_width=None):
        if not have_tabulate:
            raise Exception("You need to install the tabulate module to use the `show()` method")
        data = [("id", self.id)] + [(field.name, getattr(self, field.name, None))
                                    for field in self.fields]
        if max_width:
            value_column_width = max_width - max(len(item[0]) for item in data)

            def fit_column(value):
                strv = str(value)
                if len(strv) > value_column_width:
                    strv = strv[:value_column_width - 4] + " ..."
                return strv
            data = [(k, fit_column(v)) for k, v in data]
        print(tabulate(data, tablefmt="plain"))
        #return tabulate(data, tablefmt='html') - also see  https://bitbucket.org/astanin/python-tabulate/issues/57/html-class-options-for-tables

    @classmethod
    def generate_query(cls, query_id, client, resolved=False, top_level=True,
                       field_names_used=None, parents=None):
        # todo: don't include "alternatives" fields in resolved queries,
        #       at it makes the queries really large
        #       such connections can always be resolved manually
        #print(cls, top_level, field_names_used)
        if top_level:
            fields = [{
                "relative_path": "@id",
                "filter": {
                    "op": "equals",
                    "parameter": "id"
                }
            }]
        else:
            fields = [{"relative_path": "@id"}]
        fields.append({"relative_path": "@type"})
        if field_names_used is None:
            field_names_used = []

        for field in cls.fields:
            #print("  handling field {}".format(field))

            # set parents to avoid infinite recursion
            if top_level:
                # reset for each field
                parents = set([cls])
            else:
                parents.add(cls)

            if field.intrinsic:
                field_definition = {
                    "fieldname": field.path,
                    "relative_path": expand_uri(field.path, cls.context, client)[0],
                }
                field_names_used.append(field.path)
                if top_level:
                    if field.name == "name":
                        field_definition["sort"] = True
                        if field.required:
                            field_definition["required"] = True

                if any(issubclass(_type, KGObject) for _type in field.types):

                    if not top_level and field.path in field_names_used:
                        field_definition["fieldname"] = "{}__{}".format(cls.__name__, field.path)
                    if field.multiple:
                        field_definition["ensure_order"] = True

                    field_definition["fields"] = [
                        {"relative_path": "@id"},
                        {"relative_path": "@type"}
                    ]

                    if resolved and not parents.intersection(set(field.types)):
                        #               ^^^ avoid recursion to types seen previously
                        #print("    resolving.... (parents={}, field.types={})".format(parents, field.types))
                        subfield_map = {}
                        for child_cls in field.types:
                            subfields = child_cls.generate_query(
                                query_id, client, resolved=resolved,
                                top_level=False, field_names_used=field_names_used,
                                parents=copy(parents))  # use a copy to keep the original for the next iteration
                            subfield_map.update(
                                {subfield_defn.get("fieldname", subfield_defn["relative_path"]): subfield_defn
                                 for subfield_defn in subfields}
                            )
                        field_definition["fields"] = list(subfield_map.values())
                elif any(issubclass(_type, OntologyTerm) for _type in field.types):
                    if not top_level and field.path in field_names_used:
                        field_definition["fieldname"] = "{}__{}".format(cls.__name__, field.path)
                    field_definition["fields"] = [
                        {"relative_path": "@id"},
                        {
                            "fieldname": "label",
                            "relative_path": "http://www.w3.org/2000/01/rdf-schema#label"
                        }
                    ]
                elif issubclass(field.types[0], StructuredMetadata) and hasattr(field.types[0], "fields"):
                    field_definition["fields"] = [
                        {
                            "fieldname": subfield.name,
                            "relative_path": expand_uri(subfield.path, field.types[0].context)[0]
                        }
                        for subfield in field.types[0].fields
                    ]

                # here we add a filter for top-level fields
                if field.types[0] in (int, float, bool, datetime, date):
                    op = "equals"
                else:
                    op = "contains"
                if top_level:
                    field_definition["filter"] = {  # don't filter on datetime,  ...
                        "op": op,
                        "parameter": field.name
                    }

                fields.append(field_definition)

            # todo: add proxy reverse links for non-intrinsic fields?
            #       (proxy because otherwise we risk returning the entire graph!)
        if top_level:
            query = {
                "https://schema.hbp.eu/graphQuery/root_schema": {
                    "@id": "{}/schemas/{}".format(client.nexus_endpoint, cls.path)
                },
                "http://schema.org/identifier": "{}/{}".format(cls.path, query_id),
                "fields": fields,
                "@context": {
                    "fieldname": {
                        "@type": "@id",
                        "@id": "fieldname"
                    },
                    "schema": "http://schema.org/",
                    "@vocab": "https://schema.hbp.eu/graphQuery/",
                    "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
                    "merge": {
                        "@type": "@id",
                        "@id": "merge"
                    },
                    "query": "https://schema.hbp.eu/myQuery/",
                    "dcterms": "http://purl.org/dc/terms/",  # don't think we need this
                    "relative_path": {
                        "@type": "@id",
                        "@id": "relative_path"
                    }
                }
            }
            return query
        else:
            return fields

    @classmethod
    def store_queries(cls, client):
        for query_id, resolved in (("fgSimple", False), ("fgResolved", True)):
            query_definition = cls.generate_query(query_id, client, resolved=resolved)
            path = "{}/{}".format(cls.path, query_id)
            try:
                client.store_query(path, query_definition)
            except HTTPError as err:
                if err.response.status_code == 401:
                    warnings.warn("Unable to store query to {} with id '{}': {}".format(
                        path, query_id, err.response.text))
                else:
                    raise

    @classmethod
    def retrieve_query(cls, query_id, client):
        path = "{}/{}".format(cls.path, query_id)
        return client.retrieve_query(path)

    def is_released(self, client):
        """Release status of the node"""
        return client.is_released(self.id)

    def release(self, client):
        """Release this node (make it available in public search)."""
        return client.release(self.id)

    def unrelease(self, client):
        """Urelease this node (remove it from public search)."""
        return client.unrelease(self.id)


class MockKGObject(KGObject):
    """Mock version of KGObject, useful for testing."""

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return 'MockKGObject({}, {})'.format(self.type, self.id)


def cache(f):
    @wraps(f)
    def wrapper(cls, instance, client, use_cache=True, resolved=False):
        if use_cache and instance.data["@id"] in KGObject.object_cache:
            obj = KGObject.object_cache[instance.data["@id"]]
            #print(f"Found in cache: {obj.id}")
            return obj
        else:
            obj = f(cls, instance, client, resolved=resolved)
            KGObject.object_cache[obj.id] = obj
            #print(f"Added to cache: {obj.id}")
            return obj
    return wrapper


class StructuredMetadata(with_metaclass(Registry, object)):
    """Abstract base class"""
    pass


class OntologyTerm(StructuredMetadata):
    """docstring"""

    def __init__(self, label, iri=None, strict=False):
        self.label = label
        self.iri = iri or self.iri_map.get(label)
        if strict:
            if self.iri is None:
                raise ValueError("No IRI found for label {}".format(label))

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.label!r}, {self.iri!r})'.format(self=self))

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self.label == other.label
                and self.iri == other.iri)

    def to_jsonld(self, client=None):
        return {'@id': self.iri,
                'label': self.label}

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        if "http://www.w3.org/2000/01/rdf-schema#label" in data:
            # workaround for an issue with LivePaper.license
            data["label"] = data["http://www.w3.org/2000/01/rdf-schema#label"]
        return cls(data["label"], data["@id"])

    @classmethod
    def terms(cls):
        return list(cls.iri_map.keys())


class KGProxy(object):
    """docstring"""

    def __init__(self, cls, uri):
        if isinstance(cls, str):
            self.cls = lookup(cls)
        elif cls is None:
            self.cls = lookup_by_id(uri)
        else:
            self.cls = cls
        self.id = uri

    @property
    def type(self):
        try:
            return self.cls.type
        except AttributeError as err:
            raise AttributeError(f"{err} self.cls={self.cls}")

    @property
    def classes(self):
        # For consistency with KGQuery interface
        if isinstance(self.cls, (list, tuple)):
            return self.cls
        else:
            return [self.cls]

    def resolve(self, client, api="query", scope="released", use_cache=True, follow_links=0):
        """docstring"""
        if use_cache and self.id in KGObject.object_cache:
            obj = KGObject.object_cache[self.id]
            #if obj:
            #    logger.debug("Retrieving object {} from cache. Status: {}".format(self.id, obj._build_data(client)))
        else:
            if len(self.classes) > 1:
                obj = None
                for cls in self.classes:
                    obj = cls.from_uri(self.id, client, api=api, scope=scope)
                    if obj is not None:
                        break
            else:
                obj = self.cls.from_uri(self.id, client, api=api, scope=scope)
            if obj is None:
                raise Exception(f"Cannot resolve proxy object {self.id} as {self.classes}")
            KGObject.object_cache[self.id] = obj
        if follow_links > 0:
            return obj.resolve(
                client, api=api, scope=scope, use_cache=use_cache,
                follow_links=follow_links
            )
        else:
            return obj

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.classes!r}, {self.id!r})'.format(self=self))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.cls == other.cls and self.id == other.id

    def __ne__(self, other):
        return (not isinstance(other, self.__class__)
                or self.cls != other.cls
                or self.id != other.id)

    @property
    def uuid(self):
        return self.id.split("/")[-1]

    def delete(self, client):
        """Delete the instance which this proxy represents"""
        obj = self.resolve(client)
        if obj:
            obj.delete(client)


class KGQuery(object):
    """docstring"""

    def __init__(self, classes, filter, context):
        self.classes = []
        for cls in as_list(classes):
            if isinstance(cls, str):
                self.classes.append(lookup(cls))
            else:
                self.classes.append(cls)
        self.filter = filter
        self.context = context

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.classes!r}, {self.filter!r})'.format(self=self))

    def resolve(self, client, size=10000, from_index=0, api="query", scope="released", 
                use_cache=True, follow_links=0):
        # todo: add from_index argument?
        objects = []
        for cls in self.classes:
            if api == "nexus":
                instances = client.query_nexus(
                    path=cls.path,
                    filter=self.filter["nexus"],
                    context=self.context,
                    size=size,
                    from_index=from_index
                )
            elif api == "query":
                instances = client.query_kgquery(
                    path=cls.path,
                    query_id=cls.query_id,
                    filter=self.filter["query"],
                    size=size,
                    from_index=from_index,
                    scope=scope)
            else:
                raise ValueError("'api' must be either 'nexus' or 'query'")
            objects.extend(cls.from_kg_instance(instance, client)
                           for instance in instances)
        for obj in objects:
            KGObject.object_cache[obj.id] = obj
        if follow_links > 0:
            for obj in objects:
                obj.resolve(
                    client, api=api, scope=scope, use_cache=use_cache,
                    follow_links=follow_links
                )
        if len(objects) == 1:
            return objects[0]
        else:
            return objects

    def count(self, client, api="query", scope="released"):
        n = 0
        for cls in self.classes:
            if api == "nexus":
                n += client.count_nexus(
                    path=cls.path,
                    filter=self.filter["nexus"],
                    context=self.context
                )
            elif api == "query":
                raise NotImplementedError("todo")
            else:
                raise ValueError("'api' must be either 'nexus' or 'query'")
        return n


class IRI(object):

    def __init__(self, value):
        if isinstance(value, IRI):
            value = value.value
        if not value.startswith("http"):
            raise ValueError("Invalid IRI")
        self.value = value

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

    def __repr__(self):
        return f"IRI(self.value)"

    def __str__(self):
        return self.value

    def to_jsonld(self, client):
        return {"@id": self.value}


class Distribution(StructuredMetadata):

    def __init__(self, location, size=None, digest=None, digest_method=None, content_type=None,
                 original_file_name=None):
        if "@id" in location:
            location = location["@id"]
        if not isinstance(location, str):
            # todo: add check that location is a URI
            raise ValueError("location must be a URI")
        self.location = location
        self.size = size
        self.digest = digest
        self.digest_method = digest_method
        self.content_type = content_type
        self.original_file_name = original_file_name

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.location!r}, digest="{self.digest}")'.format(self=self))

    def __eq__(self, other):
        if isinstance(other, Distribution):
            return all(getattr(self, field) == getattr(other, field)
                       for field in ("location", "size", "digest", "digest_method",
                                     "content_type", "original_file_name"))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        if "contentSize" in data:
            size = data["contentSize"]["value"]
            if data["contentSize"]["unit"] != "byte":
                raise NotImplementedError()
        else:
            size = None
        if "digest" in data:
            digest = data["digest"]["value"]
            digest_method = data["digest"].get("algorithm")
        else:
            digest = None
            digest_method = None
        if "downloadURL" in data:
            download_url = data["downloadURL"]
        else:
            download_url = data["http://schema.org/downloadURL"]
        return cls(download_url, size, digest, digest_method, data.get("mediaType"),
                   data.get("originalFileName"))

    def to_jsonld(self, client):
        data = {
            "@context": "{{base}}/contexts/nexus/core/distribution/v0.1.0".replace("{{base}}", client.nexus_endpoint),
            "downloadURL": self.location
        }
        if self.size:
            data["contentSize"] = {
                "unit": "byte",
                "value": self.size
            }
        if self.digest:
            data["digest"] = {
                "algorithm": self.digest_method,  # e.g. "SHA-256"
                "value": self.digest
            }
        if self.content_type:
            data["mediaType"] = self.content_type
        if self.original_file_name:  # not sure if this is part of the schema, or just an annotation
            data["originalFileName"] = self.original_file_name
        return data

    def download(self, local_directory, client):
        if not os.path.isdir(local_directory):
            os.makedirs(local_directory, exist_ok=True)
        headers = client._nexus_client._http_client.auth_client.get_headers()
        response = requests.get(self.location, headers=headers)
        if response.status_code == 200:
            local_file_name = self.original_file_name or self.location.split("/")[-1]
            with open(os.path.join(local_directory, local_file_name), "wb") as fp:
                fp.write(response.content)
        else:
            raise IOError(str(response.content))

    def read(self, client):
        #headers = client._nexus_client._http_client.auth_client.get_headers()
        #response = requests.get(self.location, headers=headers)
        response = requests.get(self.location)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            raise IOError(str(response.content))


def build_kg_object(cls, data, resolved=False, client=None):
    """
    Build a KGObject, a KGProxy, or a list of such, based on the data provided.

    This takes care of the JSON-LD quirk that you get a list if there are multiple
    objects, but you get the object directly if there is only one.

    Returns `None` if data is None.
    """
    if data is None:
        return None

    if not isinstance(data, list):
        if not isinstance(data, dict):
            raise ValueError("data must be a list or dict")
        if "@list" in data:
            assert len(data) == 1
            data = data["@list"]
        else:
            data = [data]

    objects = []
    for item in data:
        if item is None:
            logger.error(f"Unexpected null. cls={cls} data={data}")
            continue
        logger.debug(f"Building {cls} from {item.get('@id', 'not a node')}")
        if cls is None:
            # note that if cls is None, then the class can be different for each list item
            # therefore we need to use a new variable kg_cls inside the loop
            if "@type" in item:
                try:
                    kg_cls = lookup_type(item["@type"])
                except KeyError:
                    kg_cls = lookup_type(compact_uri(item["@type"], standard_context))
            elif "label" in item:
                kg_cls = lookup_by_iri(item["@id"])
            # todo: add lookup by @id
            else:
                raise ValueError("Cannot determine type. Item was: {}".format(item))
        else:
            kg_cls = cls

        if isinstance(kg_cls, list):
            assert all(issubclass(item, KGObject) for item in kg_cls)
            if resolved:
                raise NotImplementedError
            else:
                obj = KGProxy(kg_cls, item["@id"])
        elif issubclass(kg_cls, StructuredMetadata):
            obj = kg_cls.from_jsonld(item)
        elif issubclass(kg_cls, KGObject):
            if "@id" in item and item["@id"].startswith("http"):
                # here is where we check the "resolved" keyword,
                # and return an actual object if we have the data
                # or resolve the proxy if we don't
                if resolved:
                    if kg_cls.namespace is None:
                        kg_cls.namespace = namespace_from_id(item["@id"])
                    try:
                        instance = Instance(kg_cls.path, item, Instance.path)
                        obj = kg_cls.from_kg_instance(instance, client, resolved=resolved)
                    except (ValueError, KeyError) as err:
                        # to add: emit a warning
                        logger.warning("Error in building {}: {}".format(kg_cls.__name__, err))
                        obj = KGProxy(kg_cls, item["@id"]).resolve(
                            client,
                            api=item.get("fg:api", "query"))
                else:
                    if "@type" in item and item["@type"] is not None and kg_cls not in as_list(
                            lookup_type(compact_uri(item["@type"], standard_context))):
                        logger.warning("Mismatched types")
                        obj = None
                    else:
                        obj = KGProxy(kg_cls, item["@id"])
            else:
                # todo: add a logger.warning that we have dud data
                obj = None
        else:
            raise ValueError("cls must be a subclass of KGObject or StructuredMetadata")
        if obj is not None:
            objects.append(obj)

    if len(objects) == 1:
        return objects[0]
    else:
        return objects


# An upload function used by all entity classes -> to be moved in "utils"
def upload_attachment(cls, file_path, client):
    assert os.path.isfile(file_path)
    statinfo = os.stat(file_path)
    if statinfo.st_size > ATTACHMENT_SIZE_LIMIT:
        raise Exception("File is too large to store directly in the KnowledgeGraph, please upload it to a Swift container")
    # todo, use the Nexus HTTP client directly for the following
    headers = client._nexus_client._http_client.auth_client.get_headers()
    content_type, encoding = mimetypes.guess_type(file_path, strict=False)
    response = requests.put("{}/attachment?rev={}".format(cls.id, cls.rev or 1),
                            headers=headers,
                            files={
                                "file": (os.path.basename(file_path),
                                        open(file_path, "rb"),
                                        content_type)
                            })
    if response.status_code < 300:
        logger.info("Added attachment {} to {}".format(file_path, cls.id))
        cls._file_to_upload = None
        cls.report_file = Distribution.from_jsonld(response.json()["distribution"][0])
    else:
        raise Exception(str(response.content))


class HasAliasMixin(object):

    @classmethod
    def from_alias(cls, alias, client, api="query", scope="released"):
        context = {
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"
        }
        query = {
            "nexus": {
                "path": "nsg:alias",
                "op": "eq",
                "value": alias
            },
            "query": {
                "alias": alias
            }
        }
        return KGQuery(cls, query, context).resolve(client, api=api, scope=scope)
