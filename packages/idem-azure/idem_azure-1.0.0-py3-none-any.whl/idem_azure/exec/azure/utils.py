# -*- coding: utf-8 -*-
"""
Utilities for exec and states APIs.

Copyright (c) 2021 VMware, Inc.
SPDX-License-Identifier: Apache-2.0
"""


from collections import Mapping
from functools import wraps


def _put(hub, o, *subkeys: (str)):
    """
    Sets on the hub, object o, based on a unique key o's formed
    bh the subkey set.
    :param o: An object to place on the hub.
    :param subkeys: Set of strings that, in order, make a unique key.
    The subkeys should be suficient to produce unique key for o in all cases.
    For example:
        hub.exec.azure.util.set_on_hub(o, "my_resoruce_group", "my_vm")
    """
    key = ".".join(subkeys)
    hub.exec.azure.OBJECT_CACHE[key] = o
    return {"result": True, "comment": "", "ret": None}


def _get(hub, *subkeys: (str)):
    """
    Gets an azure object from the hub based resource_group and name
    (which should be unique in all cases).
    :param subkeys: Tuple of strings that, in order, make a unique key.

    For example:
        subkeys = ("my_rg", "my_virtual_network", "my_subnet",
        "my_subnet_name")

        hub.tool.azure.utils._get(hub, subkeys)
    """
    key = ".".join(subkeys)
    try:
        ret = hub.exec.azure.OBJECT_CACHE[key]
    except KeyError:
        ret = None

    return ret


async def transform_object(hub, ctx, obj, xform_func, *keys):
    """
    Looks for resource_id keys in an object and checks if the value is a
    str or subkey strs. If the latter, the value of the key is replaced with
    whatever a call to xform_func returns when provided they subeys.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param obj: Any Azure Resource Management object (as_dict()).
    :param xform_func: A transformation function that transforms tuple to string.
    :param keys: A list of keys to transform.
    :return: True if any object was altered, false otherwise.
    """
    ret = { "result": False, "ret": obj, "comment": ""}

    if isinstance(obj, Mapping):
        for k, v in obj.items():
            if k in keys:
                obj[k] = await xform_func(hub, ctx, v)
                ret["ret"] = obj[k]
                ret["result"] = True
            else:
                vret = await transform_object(hub, ctx, v, xform_func, *keys)
                if vret["result"]:
                    ret["result"] = True
                    obj[k] = vret["ret"]
    elif isinstance(obj, list) or isinstance(obj, tuple):
        for idx in range(len(obj)):
            vret = await transform_object(hub, ctx, obj[idx], xform_func, *keys)
            if vret["result"]:
                ret["result"] = True
    elif isinstance(obj, set):
        for o in obj:
            vret = await transform_object(hub, ctx, o, xform_func, *keys)
            if vret["result"]:
                ret["result"] = True
                o = vret["ret"]
    return ret


def _cache_put(func):
    """
    Decorator function to place an object onto the internal Azure cloud object
    cache and thereafter return the object.
    :param func: The function to decorate.
    """
    @wraps(func)
    async def wrapper(hub, ctx, list_func, *subkeys, **kwargs):
        """
        Returns, after placing on the internal cache, an existing object (if
        any) from Azure cloud.
        :param hub: The redistributed pop central hub.
        :param ctx: A dict with the keys/values for the execution of the Idem run
        located in `hub.idem.RUNS[ctx['run_name']]`.
        :param list_func: The hub (exec) function provising a list of objects.
        :param subkeys: A set of strings making up the unique key, with the
        last in the list representing the instance name of the Azure object.
        :param kwargs: Keyward parameters. Useful keywords:
            use_cache: If set, the call will use the internal cache of Azure
            objects.

        For example:
            ret = hub.exec.azure.utils.get_existing(
                ctx, hub.exec.azure.compute.virtual_machines.list,
                "my_rg", "my_vm"
            )
        """
        if "use_cache" in kwargs and kwargs["use_cache"]:
            o = _get(hub, *subkeys)
        else:
            o = None

        if o:
            ret = {"result": True, "ret": o, "comment": ""}
        else:
            ret = await func(hub, ctx, list_func, *subkeys)
            if hasattr(ret["ret"], "as_dict"):
                ret["ret"] = ret["ret"].as_dict()
            _put(hub, ret["ret"], *subkeys)

        return ret
    return wrapper


@_cache_put
async def get_existing(hub, ctx, list_func, *subkeys):
    """
    Obtains an existing object (if any) from Azure cloud.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param list_func: The hub (exec) function provising a list of objects.
    :param subkeys: A set of strings making up the unique key, with the last
    of the lest representing the instance name of the object in Azure.
    :param kwargs: Keyward parameters. Useful keywords:
        use_cache: If set, the call will use the internal cache of Azure objects.

    For example:
        ret = hub.exec.azure.utils.get_existing(ctx,
        hub.exec.azure.compute.virtual_maachines.list,
        "my_rg", "my_vm")
    """
    ret = await list_func(ctx, *subkeys[:-1])
    lret = hub.tool.azure.utils.get_from_list(
        ret["ret"], {"name": subkeys[-1]})
    return { "result": True, "ret": lret, "comment": "" }


async def get_existing_id(hub, ctx, list_func, *subkeys):
    """
    Obtains an existing object (if any) from Azure cloud and returns it's id.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param list_func: The hub (exec) function provising a list of objects.
    :param subkeys: A set of strints making up the unique key, with the last

    For example:
        ret = hub.exec.azure.utils.get_existing(ctx,
        hub.exec.azure.compute.virtual_maachines.list,
        "my_rg", "my_vm")
    """
    if len(subkeys) < 2:
        ret = {"result": True, "ret": subkeys[0], "comment": ""}
    else:
        ret = await get_existing(hub, ctx, list_func, *subkeys, use_cache=True)
        ret["ret"] = ret["ret"]["id"]
    return ret