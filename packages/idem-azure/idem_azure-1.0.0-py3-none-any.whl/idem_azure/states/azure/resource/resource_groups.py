# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management state module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements states related to ARM resources.resource_groups.
Azure credentials must be presented via the `acct Sub`_.

TODO: Document the use of cloud_environment in the acct (yaml) data file.

.. _acct Sub: https://pypi.org/project/acct
"""

from __future__ import absolute_import
from attr import fields
from dict_tools import differ
import copy

# Import plugin helpers
import idem_azure.helpers.exc as idemexc
from idem_azure.helpers.returns import StateReturn


async def present(hub, ctx, name, resource_group_name, parameters, **kwargs):
    """Ensure a resource group exists pursuant to the requested state.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure resource group present").
    :param resource_group_name:  Name of the resource group.
    :param location: The Azure location in which to create the resource
    group. This is unmodifiable once the group is created.

    Example usage:
    .. code-block:: yaml
        Ensure Resource Group Exists:
            azure.resource.resource_groups.present:
                - resource_group_name: rg_prod
                - location: eastus
                tags:
                    environmant: prod
    """
    exec_ret = await hub.exec.azure.resource.resource_groups.check_existence(
        ctx, resource_group_name
    )
    if exec_ret["ret"]:
        action = "update"
        # Get the old (existing) instance
        exec_ret = await hub.exec.azure.resource.resource_groups.get(
            ctx, resource_group_name
        )
        old = exec_ret["ret"]
        update = copy.deepcopy(old)
        update.update(parameters)
        changes = not hub.tool.azure.utils.is_within(old, parameters)
    else:
        action = "create"
        old = {}
        update = parameters
        changes = True

    if not changes:
        ret = StateReturn(
            name=name, result=True,
            comment = f"Resource group {resource_group_name} is already present."
        )
    elif ctx["test"]:
        ret = StateReturn(
            name = name,
            old_obj = old, new_obj = update,
            comment = f"Resource group {resource_group_name} tags would be updated."
        )
    else:
        # Need to update the existing instance with new tags spec.
        exec_ret = await hub.exec.azure.resource.resource_groups.create_or_update(
            ctx,
            resource_group_name,
            parameters,
            **kwargs
        )
        ret = StateReturn(
            name = name, result = True,
            old_obj = old, new_obj = exec_ret["ret"],
            comment = f"Resource group {resource_group_name} has been {action}d."
        )

    return ret


async def absent(hub, ctx, name, resource_group_name, **kwargs):
    """
    Ensure a resource group does not exist in the current subscription.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure resource group present").
    :param resource_group_name: Name of the resource group.

    Example usage:

    .. code-block: yaml

        Ensure Resource Group Absent:
            azure.resource.resource_groups.absent:
              - resource_group_name: {{ rg_name }}
    """
    exec_ret = await hub.exec.azure.resource.resource_groups.check_existence(
        ctx, resource_group_name
    )
    if not exec_ret["ret"]:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Resource group {resource_group_name} already absent."
        )
    elif ctx["test"]:
        ret = StateReturn(
            name = name,
            comment = f"Resource group {resource_group_name} would be deleted."
        )
    else:
        # Get the existing instance.
        old_ret = await hub.exec.azure.resource.resource_groups.get(ctx, resource_group_name)

        # Delete the existing instance.
        del_ret = await hub.exec.azure.resource.resource_groups.begin_delete(
            ctx, resource_group_name, **kwargs
        )
        ret = StateReturn(
            name = name, result = True,
            old_obj = old_ret["ret"], new_obj = {},
            comment = f"Resource group {resource_group_name} delete in progress."
        )

    return ret
