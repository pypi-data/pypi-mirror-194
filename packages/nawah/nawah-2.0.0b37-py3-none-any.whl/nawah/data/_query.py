import copy
import logging
from typing import TYPE_CHECKING, Any, MutableMapping, Optional, Tuple, Union

from nawah.classes import Var
from nawah.config import Config

if TYPE_CHECKING:
    from nawah.classes import Attr, Query
    from nawah.types import (NawahQueryOperAnd, NawahQueryOperOr,
                             NawahQuerySpecialGroup, NawahQueryStep)

logger = logging.getLogger("nawah")


def _compile_query(
    *,
    attrs: MutableMapping[str, "Attr"],
    query: "Query",
) -> Tuple[
    Optional[int],
    Optional[int],
    MutableMapping[str, int],
    list[Any],
    dict[str, bool],
    list[Any],
]:
    skip: Optional[int] = None
    limit: Optional[int] = None
    sort: MutableMapping[str, int] = {"_id": -1}
    logger.debug("attempting to process query: %s", query)

    filter: list[Any] = []
    project: dict[str, bool] = {}
    lookup: list[Any] = []

    query = copy.deepcopy(query)

    # Update variables per Query Special Args
    if "$deleted" in query and query["$deleted"] is True:
        filter.append({"__deleted": {"$exists": True}})
    else:
        filter.append({"__deleted": {"$exists": False}})
    if "$skip" in query:
        skip = query["$skip"]
    if "$limit" in query:
        limit = query["$limit"]
    if "$sort" in query:
        sort = query["$sort"]

    for step in query.pipe or []:
        _compile_query_step(
            query=query,
            attrs=attrs,
            filter=filter,
            lookup=lookup,
            step=step,
        )

    if "$attrs" in query and isinstance(query["$attrs"], list):
        project = {attr: True for attr in query["$attrs"] if attr in attrs.keys()}
    else:
        project = {attr: True for attr in attrs.keys()}

    return (skip, limit, sort, filter, project, lookup)


def _compile_query_step(
    *,
    query: "Query",
    attrs: MutableMapping[str, "Attr"],
    step: Union["NawahQueryStep", "NawahQueryOperOr", "NawahQueryOperAnd"],
    filter: list[Any],
    lookup: list[Any],
    append_query: bool = True,
) -> None:
    if append_query:
        filter.append(step)

    attr_name = list(step)[0]
    attr_val = step[attr_name]  # type: ignore

    if isinstance(attr_val, list):
        for child_attr_val in attr_val:
            _compile_query_step(
                query=query,
                attrs=attrs,
                step=child_attr_val,
                filter=filter,
                lookup=lookup,
                append_query=False,
            )
        return

    if "." not in attr_name:
        return

    root_attr_name = attr_name.split(".")[0]

    if root_attr_name not in attrs or not attrs[root_attr_name].extn:
        return

    # [TODO] Check if this works with EXTN as Attr Type TYPE
    # Don't attempt to extn attr that is already extended
    if isinstance(attrs[root_attr_name].extn.module, Var):
        extn_collection = (
            f'{query[f"{attrs[root_attr_name].extn.module.var}:$eq"][0]}_docs'
        )
    else:
        extn_collection = Config.modules[attrs[root_attr_name].extn.module].collection
    lookup_entry = {
        "collection": extn_collection,
        "query": {attr_name.replace(f"{root_attr_name}.", ""): attr_val},
        "results": ["NONE"],
    }
    lookup.append(lookup_entry)
    step[root_attr_name] = {"$in": lookup_entry["results"]}
    del step[attr_name]
