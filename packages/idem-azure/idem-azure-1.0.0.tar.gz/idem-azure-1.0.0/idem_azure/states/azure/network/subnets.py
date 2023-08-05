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


# Import plugin helpers
import idem_azure.helpers.exc as idemexc
from idem_azure.helpers.returns import StateReturn


async def present(hub, ctx, name, resource_group_name,
    virtual_network_name, subnet_name, subnet_parameters,
    **kwargs
):
    """
    Ensure a subnet exists pursuant to the requested state.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure subnet present").
    :param resource_group_name: Name of the resource group.
    :param virtual_network_name: Name of the virtual network.
    :param subnet_name: Name of the subnet.
    :param parameters: `Subnet`_ parameter dictionary.
    :param kwargs: Keyword args passed direclty to the Azure SDK API.

    Example usage:
    .. code-block:: yaml
        Assure Subnet Present:
            azure.network.subnets.present:
                - resource_group_name: {{ rg_name }}
                - virtual_network_name: {{ vnet_name }}
                - subnet_name: {{ subnet_name }}
                - subnet_parameters:
                    address_prefix: "10.0.0.0/24"

    .. _Subnet: https://docs.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.v2020_06_01.models.subnet?view=azure-python
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.subnets.list,
            resource_group_name, virtual_network_name, subnet_name
        )
        action = "update"
        old = exec["ret"]
        update = copy.deepcopy(old)
        update.update(subnet_parameters)
        changes = not hub.tool.azure.utils.is_within(old, subnet_parameters)
    except idemexc.NotFoundError:
        old = {}
        update = subnet_parameters
        action = "create"
        changes = True

    if not changes:
        ret = StateReturn(
            name=name, result=True,
            comment = f"Subnet {subnet_name} is already present."
        )
    elif ctx["test"]:
        ret = StateReturn(
            name=name,
            old_obj = old, new_obj = update,
            comment = f"Subnet {subnet_name} would be {action}d."
        )
    else:
        exec = await hub.exec.azure.network.subnets.begin_create_or_update(
            ctx,
            resource_group_name,
            virtual_network_name,
            subnet_name,
            update,
            **kwargs
        )
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.subnets.list,
            resource_group_name, virtual_network_name, subnet_name
        )
        ret = StateReturn(
            name = name, result = True,
            old_obj = old, new_obj = exec["ret"],
            comment = f"Subnet {subnet_name} has been {action}d."
        )

    return ret


async def absent(hub, ctx, name, resource_group_name,
                virtual_network_name, subnet_name, **kwargs
):
    """
    Ensure a subnet does not exist in the current subscription.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure subnet present").:param resource_group_name: Name of the resource group.
    :param resource_group_name: Name of the resource group.
    :param virtual_network_name: Name of virtual network owning the subnet.
    :param subnet_name: Name of the subnet to assure absence.
    :param kwargs: Keyword args passed direclty to the Azure SDK API.

    Example usage:

    .. code-block: yaml

        Ensure Subnet Absent:
            azure.network.subnets.absent:
              - resource_group_name: {{ rg_group }}
              - virtual_network_name: {{ network_name }}
              - subnet_name: {{ subnet_name }}
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.subnets.list,
            resource_group_name, virtual_network_name, subnet_name,
        )
        if ctx["test"]:
            ret = StateReturn(
                name = name,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Subnet {subnet_name} would be deleted."
            )
        else:
            del_exec = await hub.exec.azure.network.virtual_networks.begin_delete(
                ctx,
                resource_group_name,
                virtual_network_name,
                **kwargs
            )
            ret = StateReturn(
                name = name, result = True,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Subnet {subnet_name} delete in progress."
            )
    except idemexc.NotFoundError:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Subnet {subnet_name} already absent."
        )

    return ret
