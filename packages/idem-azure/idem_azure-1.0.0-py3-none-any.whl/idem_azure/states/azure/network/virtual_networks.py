# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management state module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements states related to ARM network.virtual_networks.
Azure credentials must be presented via the `acct Sub`_.

TODO: Document the use of cloud_environment in the acct (yaml) data file.

.. _acct Sub: https://pypi.org/project/acct
"""


import copy
from dict_tools import differ


import idem_azure.helpers.exc as idemexc
from idem_azure.helpers.returns import StateReturn

async def present(hub, ctx, name, resource_group_name,
                virtual_network_name, parameters, **kwargs):
    """
    Ensure a virtual_network exists pursuant to the requested state.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure vnet present").
    :param resource_group_name: Name of the resource group.
    :param virtual_network_name: Name of the virtual network.
    :param parameters: `VirtualNetwork`_ parameter dictionary.
    :param kwargs: Keyword args passed direclty to the Azure SDK API.

    Example usage:
    .. code-block:: yaml
        Assure Virtual Network Present:
            azure.network.virtual_networks.present:
                - resource_group_name: {{ rg_name }}
                - virtual_network_name: {{ vnet_name }}
                - parameters:
                    location: {{ location }}
                    address_space:
                    address_prefixes:
                        - "10.0.0.0/16"

    .. _VirtualNetwork: https://docs.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.v2020_06_01.models.virtualnetwork?view=azure-python
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.virtual_networks.list,
            resource_group_name, virtual_network_name
        )
        action = "update"
        old = exec["ret"]
        update = copy.deepcopy(old)
        update.update(parameters)
        changes = not hub.tool.azure.utils.is_within(old, parameters)
    except idemexc.NotFoundError:
        action = "create"
        old = {}
        update = parameters
        changes = True

    if not changes:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Virtual network {virtual_network_name} is already present."
        )
    elif ctx["test"]:
        ret = StateReturn(
            name = name, result = True,
            old_obj = old, new_obj = update,
            comment = f"Virtual Network {virtual_network_name} would be {action}d."
        )
    else:
        exec = await hub.exec.azure.network.virtual_networks.begin_create_or_update(
            ctx,
            resource_group_name,
            virtual_network_name,
            parameters,
            **kwargs
        )
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.virtual_networks.list,
            resource_group_name, virtual_network_name
        )
        ret = StateReturn(
            name = name, result = True,
            old_obj = old, new_obj = exec["ret"],
            comment = f"Virtual network {virtual_network_name} has been {action}d."
        )

    return ret


async def absent(hub, ctx, name, resource_group_name,
                virtual_network_name, **kwargs):
    """
    Ensure a virtual network does not exist in the current subscription.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure vnet present").
    :param resource_group_name: Name of the resource group.
    :param virtual_network_name: Name of the virtual network to assure absence.
    :param kwargs: Keyword args passed direclty to the Azure SDK API.

    Example usage:

    .. code-block: yaml

        Ensure virtual network absent:
            azure.network.virtual_networks.absent:
              - resource_group_name: {{ rg_name }}
              - virtual_network_name: {{ vnet_name }}
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(ctx,
            hub.exec.azure.network.virtual_networks.list,
            resource_group_name, virtual_network_name
        )
        if ctx["test"]:
            ret = StateReturn(
                name = name,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Virtual network {virtual_network_name} would be deleted."
            )
        else:
            _ = await hub.exec.azure.network.virtual_networks.begin_delete(
                ctx,
                resource_group_name,
                virtual_network_name,
                **kwargs
            )
            ret = StateReturn(
                name = name, result = True,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Virtual network {virtual_network_name} delete in progress."
            )
    except:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Virtual network {virtual_network_name} already absent."
        )

    return ret
