import copy
import logging
from typing import (TYPE_CHECKING, Any, MutableMapping, MutableSequence,
                    Optional, Union, cast)

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from nawah.classes import Query, Var
from nawah.config import Config
from nawah.enums import AttrType, Event, LocaleStrategy

from ._query import _compile_query

if TYPE_CHECKING:
    from nawah.classes import Attr, Extn
    from nawah.types import NawahDoc, NawahSession

logger = logging.getLogger("nawah")


async def read(
    *,
    session: "NawahSession",
    collection_name: str,
    attrs: MutableMapping[str, "Attr"],
    query: "Query",
    skip_process: bool = False,
    extn_attrs: MutableSequence[str] = [],
) -> MutableMapping[str, Any]:
    skip, limit, sort, filter, project, lookup = _compile_query(
        attrs=attrs, query=query
    )

    logger.debug("filter: %s", filter)
    logger.debug("project: %s", project)
    logger.debug("lookup: %s", lookup)
    logger.debug("skip, limit, sort, group: %s, %s, %s.", skip, limit, sort)

    for lookup_entry in lookup:
        lookup_query = Config.sys.conn[Config.data_name][
            lookup_entry["collection"]
        ].find(lookup_entry["query"], {"_id": True})
        async for lookup_doc in lookup_query:
            lookup_entry["results"].append(str(lookup_doc["_id"]))

    collection: AsyncIOMotorCollection = Config.sys.conn[Config.data_name][
        collection_name
    ]

    docs_total = await collection.count_documents({})
    if docs_total == 0:
        return {"total": 0, "count": 0, "docs": [], "groups": []}

    project = {"_id": True, **project}
    collection_query = collection.find(
        {"$and": filter} if len(filter) > 0 else {}, project
    )


    if sort is not None:
        collection_query = collection_query.sort(list(sort.items()))
    if skip is not None:
        collection_query = collection_query.skip(skip)
    if limit is not None:
        collection_query = collection_query.limit(limit)

    logger.debug("final query: %s, %s.", collection, collection_query)

    docs_count = await collection.count_documents(
        {"$and": filter} if len(filter) > 0 else {}
    )

    if docs_count == 0:
        return {
            "total": docs_total,
            "count": 0,
            "docs": [],
            "groups": {},
        }

    models = []
    extn_models: MutableMapping[str, Optional[MutableMapping]] = {}
    async for doc in collection_query:
        doc = {k: doc[k] if k in doc else None for k in project}
        if not skip_process:
            doc = await _process_results_doc(
                session=session,
                attrs=attrs,
                doc=doc,
                extn_models=extn_models,
                extn_attrs=extn_attrs,
            )
        if doc:
            # Explicitly convert value of _id from ObjectId to str to prevent need to handle this
            # fuzzily in other areas of Nawah
            doc["_id"] = str(doc["_id"])
            models.append(doc)

    return {
        "total": docs_total,
        "count": docs_count,
        "docs": models,
        "groups": {},
    }


async def _process_results_doc(
    *,
    session: "NawahSession",
    attrs: MutableMapping[str, "Attr"],
    doc: "NawahDoc",
    extn_models: MutableMapping[str, Optional[MutableMapping]],
    extn_attrs: MutableSequence[str],
) -> MutableMapping[str, Any]:
    # Process doc attrs
    for attr in attrs.keys():
        if attrs[attr].type == AttrType.LOCALE:
            if (
                attr in doc.keys()
                and isinstance(doc[attr], dict)
                and Config.locale in doc[attr].keys()
            ):
                if Config.locale_strategy == LocaleStrategy.NONE_VALUE:
                    doc[attr] = {
                        locale: doc[attr][locale]
                        if locale in doc[attr].keys()
                        else None
                        for locale in Config.locales
                    }
                elif callable(Config.locale_strategy):
                    doc[attr] = {
                        locale: doc[attr][locale]
                        if locale in doc[attr].keys()
                        else Config.locale_strategy(
                            attr_val=doc[attr][Config.locale], locale=locale
                        )
                        for locale in Config.locales
                    }
                else:
                    doc[attr] = {
                        locale: doc[attr][locale]
                        if locale in doc[attr].keys()
                        else doc[attr][Config.locale]
                        for locale in Config.locales
                    }

        if attr not in extn_attrs:
            continue

        await _extend_attr(
            doc=doc,
            scope=doc,
            attr_name=attr,
            attr_type=attrs[attr],
            session=session,
            extn_models=extn_models,
        )
    # Attempt to extned the doc per extns
    return doc


async def _extend_attr(
    *,
    doc: "NawahDoc",
    scope: Union[MutableMapping[str, Any], MutableSequence[Any]],
    attr_name: Union[str, int],
    attr_type: "Attr",
    session: "NawahSession",
    extn_models: MutableMapping[str, Optional[MutableMapping]],
):
    # If scope is missing attr_name skip
    if isinstance(scope, dict) and attr_name not in scope:
        return

    # Check attr_type for possible types that require deep checking for extending
    if attr_type.type == AttrType.KV_DICT:
        attr_name = cast(str, attr_name)
        scope = cast(MutableMapping[str, Any], scope)
        if scope[attr_name] and isinstance(scope[attr_name], dict):
            for child_attr in scope[attr_name]:
                # attr_type is KV_DICT where Attr Type Arg val could be extended
                await _extend_attr(
                    doc=doc,
                    scope=scope[attr_name],
                    attr_name=child_attr,
                    attr_type=attr_type.args["val"],
                    session=session,
                    extn_models=extn_models,
                )
    if attr_type.type == AttrType.TYPED_DICT:
        attr_name = cast(str, attr_name)
        scope = cast(MutableMapping[str, Any], scope)
        if scope[attr_name] and isinstance(scope[attr_name], dict):
            for child_attr in attr_type.args["dict"]:
                # attr_type is TYPED_DICT where each dict item could be extended
                await _extend_attr(
                    doc=doc,
                    scope=scope[attr_name],
                    attr_name=child_attr,
                    attr_type=attr_type.args["dict"][child_attr],
                    session=session,
                    extn_models=extn_models,
                )

    elif attr_type.type == AttrType.LIST:
        attr_name = cast(str, attr_name)
        scope = cast(MutableMapping[str, Any], scope)
        if scope[attr_name] and isinstance(scope[attr_name], list):
            for child_attr in attr_type.args["list"]:
                # attr_type is LIST where it could have KV_DICT, TYPED_DICT, ID Attrs Types that can be [deep-]extended
                if child_attr.type == AttrType.KV_DICT:
                    for child_scope in scope[attr_name]:
                        if isinstance(child_scope, dict):
                            for child_child_attr in child_scope:
                                await _extend_attr(
                                    doc=doc,
                                    scope=child_scope,
                                    attr_name=child_child_attr,
                                    attr_type=child_attr.args["val"],
                                    session=session,
                                    extn_models=extn_models,
                                )
                elif child_attr.type == AttrType.TYPED_DICT:
                    for child_scope in scope[attr_name]:
                        if isinstance(child_scope, dict):
                            for child_child_attr in child_attr.args["dict"]:
                                await _extend_attr(
                                    doc=doc,
                                    scope=child_scope,
                                    attr_name=child_child_attr,
                                    attr_type=child_attr.args["dict"][child_child_attr],
                                    session=session,
                                    extn_models=extn_models,
                                )
                elif child_attr.type == AttrType.ID:
                    for i in range(len(scope[attr_name])):
                        await _extend_attr(
                            doc=doc,
                            scope=scope[attr_name],
                            attr_name=i,
                            attr_type=child_attr,
                            session=session,
                            extn_models=extn_models,
                        )

    if not attr_type.extn:
        return

    attr_name = cast(str, attr_name)
    scope = cast(MutableMapping[str, Any], scope)
    # Attr is having Extn for _extn value, attempt to extend attr based on scope type
    if isinstance(scope[attr_name], str):
        try:
            scope[attr_name] = await _extend_doc(
                session=session,
                doc=doc,
                attr=scope[attr_name],
                extn_id=scope[attr_name],
                extn=attr_type.extn,
                extn_models=extn_models,
            )
        except Exception as e:  # pylint: disable=broad-except
            logger.error(
                "Failed to extend attr '%s' with value '%s' per Extension Instruction: '%s'",
                attr_name,
                scope[attr_name],
                attr_type.extn,
            )
            logger.error("Exception details: %s", e)

    elif isinstance(scope[attr_name], list):
        for i, extn_id in enumerate(scope[attr_name]):
            scope[attr_name][i] = await _extend_doc(
                session=session,
                doc=doc,
                attr=scope[attr_name],
                extn_id=extn_id,
                extn=attr_type.extn,
                extn_models=extn_models,
            )


async def _extend_doc(
    *,
    session: "NawahSession",
    doc: "NawahDoc",
    attr: Optional["NawahDoc"],
    extn_id: str,
    extn: "Extn",
    extn_models: MutableMapping[str, Optional[MutableMapping]],
) -> Optional[MutableMapping]:
    from nawah.utils import call, var_value

    extn_module_name: str
    # Check if extn module is dynamic value
    if isinstance(extn.module, Var):
        extn_module_name = var_value(extn.module, session=session, doc=doc)
    else:
        extn_module_name = extn.module
    extn_module = Config.modules[extn_module_name]
    # Check if extn attr set to fetch all or specific attrs
    if isinstance(extn.attrs, Var):
        extn_attrs = var_value(extn.attrs, session=session, doc=doc)
        if extn_attrs[0] == "*":
            extn_attrs = list(extn_module.attrs)
    elif extn.attrs[0] == "*":
        extn_attrs = list(extn_module.attrs)
    else:
        extn_attrs = copy.deepcopy(extn.attrs)
    # Implicitly add _id key to extn attrs so that we don't delete it in process
    if "_id" not in extn_attrs:
        extn_attrs.append("_id")
    # Set skip events
    skip_events = [Event.PERM]
    # Check value for Extn.skip_events
    if isinstance(extn.skip_events, list):
        skip_events.extend(extn.skip_events)
    elif isinstance(extn.skip_events, Var):
        skip_events.extend(var_value(extn.skip_events, session=session, doc=doc))
    # Check if extn instruction is explicitly requires second-dimension extn.
    extn_extns = []
    extn_force = False
    if isinstance(extn.force, Var):
        extn_force = var_value(extn.force, session=session, doc=doc)
    if extn.force is True:
        extn_force = True
    if extn_force:
        extn_extns = extn_attrs
    extn_query = Query(
        [{"_id": {"$eq": ObjectId(extn_id)}}], special={"$extn": extn_extns}
    )
    # Check if additional query steps are to be appended
    # Read doc if not in extn_models
    extn_model_key = str(extn_id) + "_extn_" + str(extn_extns)
    if extn_model_key not in extn_models.keys():
        extn_results = await call(
            f"{extn_module_name}/read",
            skip_events=skip_events,
            session=session,
            query=extn_query,
        )
        if extn_results["args"]["count"]:
            extn_models[extn_model_key] = extn_results["args"]["docs"][0]
        else:
            extn_models[extn_model_key] = None
    # Set attr to extn_models doc
    extn_doc = copy.deepcopy(extn_models[extn_model_key])
    # delete all unneeded keys from the resulted doc
    if extn_doc:
        extn_doc = {attr: extn_doc[attr] for attr in extn_attrs if attr in extn_doc}
    return extn_doc
