# -*- coding: utf-8 -*-
"""
Utilities for Azure Resource Management APIs.

Copyright (c) 2019-2020, EITR Technologies, LLC.
Copyright (c) 2021 VMware, Inc.
SPDX-License-Identifier: Apache-2.0
"""

# Import Python libs
from operator import itemgetter
import importlib
import logging
import six
import sys

# Import third party libs
from azure.core.paging import ItemPaged
from azure.core.exceptions import AzureError

# Import plugin helpers
import idem_azure.helpers.exc as idemexc


log = logging.getLogger(__name__)


# async def log_cloud_error(hub, client, message, **kwargs):
#     """
#     Log an Azure cloud error exception
#     """
#     arm_ll = "azure_log_level"

#     try:
#         "azure_log_level"
#         cloud_logger = getattr(log, kwargs.get("azure_log_level"))
#     except (AttributeError, TypeError):
#         cloud_logger = getattr(log, "error")

#     cloud_logger(
#         "An Azure %s CloudError has occurred: %s", client.capitalize(), message
#     )

#     return


# async def create_object_model(hub, module_name, object_name, **kwargs):
#     """
#     Assemble an object from incoming parameters.
#     """
#     object_kwargs = {}

#     try:
#         model_module = importlib.import_module(
#             "azure.mgmt.{0}.models".format(module_name)
#         )
#         # pylint: disable=invalid-name
#         Model = getattr(model_module, object_name)
#     except ImportError:
#         raise sys.exit(
#             "The {0} model in the {1} Azure module is not available.".format(
#                 object_name, module_name
#             )
#         )

#     if "_attribute_map" in dir(Model):
#         for attr, items in Model._attribute_map.items():
#             param = kwargs.get(attr)
#             if param is not None:
#                 if items["type"][0].isupper() and isinstance(param, dict):
#                     object_kwargs[attr] = await create_object_model(
#                         hub, module_name, items["type"], **param
#                     )
#                 elif items["type"][0] == "{" and isinstance(param, dict):
#                     object_kwargs[attr] = param
#                 elif items["type"][0] == "[" and isinstance(param, list):
#                     obj_list = []
#                     for list_item in param:
#                         if items["type"][1].isupper() and isinstance(list_item, dict):
#                             obj_list.append(
#                                 await create_object_model(
#                                     hub,
#                                     module_name,
#                                     items["type"][
#                                     items["type"].index("[")
#                                     + 1: items["type"].rindex("]")
#                                     ],
#                                     **list_item,
#                                 )
#                             )
#                         elif items["type"][1] == "{" and isinstance(list_item, dict):
#                             obj_list.append(list_item)
#                         elif not items["type"][1].isupper() and items["type"][1] != "{":
#                             obj_list.append(list_item)
#                     object_kwargs[attr] = obj_list
#                 else:
#                     object_kwargs[attr] = param

#     # wrap calls to this function to catch TypeError exceptions
#     return Model(**object_kwargs)


# async def compare_list_of_dicts(
#     hub, old, new, convert_id_to_name=None, key_name="name"
# ):
#     """
#     Compare lists of dictionaries representing Azure objects. Only keys found in the "new" dictionaries are compared to
#     the "old" dictionaries, since getting Azure objects from the API returns some read-only data which should not be
#     used in the comparison. A list of parameter names can be passed in order to compare a bare object name to a full
#     Azure ID path for brevity. If string types are found in values, comparison is case insensitive. Return comment
#     should be used to trigger exit from the calling function.
#     """
#     ret = {}

#     if not convert_id_to_name:
#         convert_id_to_name = []

#     if not isinstance(new, list):
#         ret["comment"] = "must be provided as a list of dictionaries!"
#         return ret

#     if len(new) != len(old):
#         ret["changes"] = {"old": old, "new": new}
#         return ret

#     try:
#         local_configs, remote_configs = [
#             sorted(config, key=itemgetter(key_name)) for config in (new, old)
#         ]
#     except TypeError:
#         ret["comment"] = "configurations must be provided as a list of dictionaries!"
#         return ret
#     except KeyError:
#         ret[
#             "comment"
#         ] = f'configuration dictionaries must contain the "{key_name}" key!'
#         return ret

#     for idx, cfg in enumerate(local_configs):
#         for key, val in cfg.items():
#             local_val = val
#             if key in convert_id_to_name:
#                 remote_val = (
#                     remote_configs[idx].get(key, {}).get("id", "").split("/")[-1]
#                 )
#             else:
#                 remote_val = remote_configs[idx].get(key)
#                 if isinstance(local_val, six.string_types):
#                     local_val = local_val.lower()
#                 if isinstance(remote_val, six.string_types):
#                     remote_val = remote_val.lower()
#             if local_val != remote_val:
#                 ret["changes"] = {"old": remote_configs, "new": local_configs}
#                 return ret

#     return ret


def paged_object_to_list(hub, o):
    """
    Extract all pages within a paged object as a list of dictionaries.
    :param hub: The redistributed pop central hub.
    :param o: Object to expand into a list, if an ItemPaged instance.
    """
    if isinstance(o, ItemPaged):
        ret = []
        while True:
            try:
                page = next(o)
                ret.append(page.as_dict())
            except StopIteration:
                break
    else:
            ret = o

    return ret


def _is_within_dict(parent, o, ignore: set):
    """
    Determine of an object is within a parent dict object.
    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    ret = True
    for k, v in o.items():
        if k in ignore:
            break
        elif k not in parent:
            ret = False
            break
        elif not _is_within(parent[k], v, ignore):
            ret = False
            break
    return ret


def _is_within_list(parent, o, ignore: set):
    """
    Determine of an object is within a parent list object.
    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    ret = True
    for oidx in range(len(o)):
        plen = len(parent)
        for pidx in range(plen):
            if _is_within(parent[pidx], o[oidx], ignore):
                parent.pop(pidx)
                break
        if plen == len(parent):
            ret = False
            break

    return ret


def _is_within_set(parent, o, ignore: set):
    """
    Determine of an object is within a parent set object.
    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    return _is_within_list(list(parent), list(o), ignore)


def _is_within(parent, o, ignore: set):
    """
    Determine of an object is within a parent object.
    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    if not isinstance(parent, type(o)):
        return False
    elif isinstance(o, dict):
        return _is_within_dict(parent, o, ignore)
    elif isinstance(o, list):
        return _is_within_list(parent, o, ignore)
    elif isinstance(o, set):
        return _is_within_set(parent, o, ignore)
    elif isinstance(o, tuple):
        return _is_within_list(parent, o, ignore)
    else:
        return parent == o


def is_within(hub, parent, o, ignore: set = {}):
    """
    Returns True if the object (o) is contained within parent (top level)
    Azure object.
    :param hub: The redistributed pop central hub. This is required in
    Idem, so while not used, must appear.
    :param parent: The object to check if contains o.
    :param o: An object to check if is within the parent object.
    :return: False if parent and o are different types or do not compare,
    otherwise True.

    For example:

    The subset:

    { name: "my_object" }

    exists within

    { something_else: "some other thing", name: "my_object" },
    """
    return _is_within(parent, o, ignore)


def get_from_list(hub, parent, o):
    """
    Returns the first object found in parent that contains o.
    :param hub: The redistributed pop central hub. This is required in
    Idem, so while not used, must appear.
    :param parent: An iterable object to search for o.
    :param o: An object the values of which must exist in one of the iterables.

    For example:

    The subset:

    { name: "my_object" }

    exists within (and would be returned)

    [
        { name: "not_my_object", something_else: "not the other thing" }
        { name: "my_object", something_else: "some other thing"},
    ]
    """
    ret =  None
    try:
        for item in parent:
            if hasattr(item, "__iter__"):
                # all relevant Azure objects have as_dict method.
                other = item
            else:
                other = item.as_dict()

            if _is_within(other, o, {}):
                ret = item.as_dict()
                break
    except AzureError as a:
        if a.error.code == "ResourceGroupNotFound" or \
            a.error.code == "ResourceNotFound":
            pass
        else:
            raise

    if ret == None:
        raise idemexc.NotFoundError(f"Item not found: {o}.")

    return ret
