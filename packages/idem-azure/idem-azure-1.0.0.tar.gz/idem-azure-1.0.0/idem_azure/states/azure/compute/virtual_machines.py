# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management state module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements states related to ARM compute.virtual_machines.
Azure credentials must be presented via the `acct Sub`_.

TODO: Document the use of cloud_environment in the acct (yaml) data file.

.. _acct Sub: https://pypi.org/project/acct
"""


import copy
from dict_tools import differ

# Import plugin helpers
import idem_azure.helpers.exc as idemexc
from idem_azure.helpers.returns import StateReturn


async def _xform_nics(hub, ctx, subkeys):
    """
    Transform a list of subkeys to network interface ids.
    :param subkeys: Either a single value, which is returned (presumed) as
    the id, or or a subkey list to use for looking up the id.
    :return: Object reslting from converting value to Id.
    """
    id_ret = await hub.exec.azure.utils.get_existing_id(
        ctx,
        hub.exec.azure.network.network_interfaces.list,
        *subkeys
    )

    return id_ret["ret"]


async def present(hub, ctx, name, resource_group_name,
    vm_name, parameters, **kwargs
):
    """
    Ensure a virtual machine exists pursuant to the requested state.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure vm present").
    :param resource_group_name: Name of the resource group.
    :param vm_name: Name of the virtual machine.
    :param parameters: `VirtualMachine`_ parameter dictionary.
    :param kwargs: Keyword args passed direclty to the Azure API.

    Example usage:
    .. code-block:: yaml
        Assure Azure VM Present:
            azure.compute.virtual_machines.present:
            - resource_group_name: {{ rg_name }}
            - vm_name: {{ vm_name }}
            - parameters:
                location: {{ location }}
                storage_profile:
                    image_reference:
                    publisher: debian
                    offer: debian-10
                    sku: 10-backports
                    version: latest
                hardware_profile:
                    vm_size: Standard_B1ls
                os_profile:
                    computer_name: {{ vm_name }}
                    admin_username: {{ vm_user_name }}
                    admin_password: {{ vm_password }}
                network_profile:
                    network_interfaces:
                    - id:
                        - {{ rg_name }}
                        - {{ nic_name }}

    .. _VirtualMachine: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.v2021_03_01.models.virtualmachine?view=azure-python
    """
    exec = await hub.exec.azure.utils.transform_object(
        ctx, parameters, _xform_nics, "id"
    )

    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.compute.virtual_machines.list,
            resource_group_name, vm_name
        )
        old = exec["ret"]
        action = "update"

        update = copy.deepcopy(old)
        update.update(parameters)
        changes = not hub.tool.azure.utils.is_within(
            old, parameters, {"admin_password", "delete_option"}
        )
    except idemexc.NotFoundError:
        old = {}
        action = "create"
        update = parameters
        changes = True

    if not changes:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Virtual Machine {vm_name} is already present."
        )
    elif ctx["test"]:
        ret = StateReturn(
            name = name,
            old_obj = old, new_obj = update,
            comment = f"Virtual Machine {vm_name} would be updated."
        )
    else:
        exec = await hub.exec.azure.compute.virtual_machines.begin_create_or_update(
            ctx,
            resource_group_name,
            vm_name,
            update,
            **kwargs)
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.compute.virtual_machines.list,
            resource_group_name, vm_name
        )
        ret = StateReturn(
            name = name, result = True,
            old_obj = old, new_obj = exec["ret"],
            comment = f"Virtual Machine {vm_name} has been {action}d."
        )

    return ret


async def absent(hub, ctx, name,
    resource_group_name, vm_name, **kwargs
):
    """
    Ensure a virtual machine does not exist in the resource group.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure vm absent").
    :param resource_group_name: Name of the resource group.
    :param vm_name: Name of the Virtual Machine.
    :param kwargs: Keyward args passed direclty to the Azure SDK API.

    Example usage:

    .. code-block: yaml

        Ensure virtual network absent:
            azure.compute.virtual_machines.absent:
              - resource_group_name: {{ rg_name }}
              - vm_name: {{ test_network }}
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.compute.virtual_machines.list,
            resource_group_name, vm_name
        )
        if ctx["test"]:
            ret = StateReturn(
                name = name,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Virtual Machine {vm_name} would be deleted."
            )
        else:
            # Delete the existing instance (async call).
            del_ret = await hub.exec.azure.compute.virtual_machines.begin_delete(
                ctx,
                resource_group_name,
                vm_name,
                **kwargs)
            ret = StateReturn(
                name = name, result = True,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Virtual Machine {vm_name} delete in progress."
            )
    except idemexc.NotFoundError:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Virtual Machine {vm_name} already absent."
        )

    return ret
