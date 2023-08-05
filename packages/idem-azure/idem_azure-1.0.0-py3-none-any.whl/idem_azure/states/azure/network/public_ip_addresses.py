# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management state module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements states related to ARM network.public_ip_addresses.
Azure credentials must be presented via the `acct Sub`_.

TODO: Document the use of cloud_environment in the acct (yaml) data file.

.. _acct Sub: https://pypi.org/project/acct
"""


import copy


# Import plugin helpers
import idem_azure.helpers.exc as idemexc
from idem_azure.helpers.returns import StateReturn


async def present(hub, ctx, name, resource_group_name,
    public_ip_address_name, parameters, **kwargs
):
    """
    Ensure a public IP exists pursuant to the requested state.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure public IP present").
    :param resource_group_name: Name of the resource group.
    :param public_ip_address_name: Name of the public IP address.
    :param parameters: `PublicIPAddress`_ parameter dictionary.
    :param kwargs: Keyword args passed direclty to the Azure SDK API.

    Example usage:
    .. code-block:: yaml
        Assure Public IP Present:
            azure.network.public_ip_address.present:
                - resource_group_name: {{ rg_name }}
                - public_ip_address_name: {{ public_ip_address_name }}
                - parameters:
                    address_prefix: "10.0.0.0/24"

    .. _PublicIPAddress: https://docs.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.v2020_06_01.models.publicipaddress?view=azure-python
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.public_ip_addresses.list,
            resource_group_name, public_ip_address_name
        )
        action = "update"
        old = exec["ret"]
        update = copy.deepcopy(old)
        update.update(parameters)
        changes = not hub.tool.azure.utils.is_within(old, parameters)
    except idemexc.NotFoundError:
        old = {}
        update = parameters
        action = "create"
        changes = True

    if not changes:
        ret = StateReturn(
            name=name, result=True,
            comment = f"Public IP Address {public_ip_address_name} is already present."
        )
    elif ctx["test"]:
        # Just return what would have changed in 'new'.
        ret = StateReturn(
            name=name,
            old_obj = old, new_obj = update,
            comment = f"Public IP Address {public_ip_address_name} would be {action}d."
        )
    else:
        exec = await hub.exec.azure.network.public_ip_addresses.begin_create_or_update(
            ctx,
            resource_group_name,
            public_ip_address_name,
            update,
            **kwargs)
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.public_ip_addresses.list,
            resource_group_name, public_ip_address_name
        )
        ret = StateReturn(
            name = name, result = True,
            old_obj = old, new_obj = exec["ret"],
            comment = f"Public IP Address {public_ip_address_name} has been {action}d."
        )

    return ret


async def absent(hub, ctx, name,
    resource_group_name, public_ip_address_name, **kwargs
):
    """
    Ensure a public IP Address does not exist in the current subscription.
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run
    located in `hub.idem.RUNS[ctx['run_name']]`.
    :param name: The name of the state (e.g., "assure public IP absent").
    :param resource_group_name: Name of the resource group.
    :param public_ip_address_name: Name of the public IP Address.

    Example usage:

    .. code-block: yaml

        Ensure Public IP absent:
            azure.network.public_ip_addresses.absent:
              - resource_group_name: test_group
              - public_ip_address_name: {{ public_ip_name }}
    """
    try:
        exec = await hub.exec.azure.utils.get_existing(
            ctx,
            hub.exec.azure.network.public_ip_addresses.list,
            resource_group_name, public_ip_address_name, **kwargs
        )
        if ctx["test"]:
            ret = StateReturn(
                name = name,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Public IP Address {public_ip_address_name} would be deleted."
            )
        else:
            _ = await hub.exec.azure.network.public_ip_addresses.begin_delete(
                ctx,
                resource_group_name,
                public_ip_address_name,
                **kwargs)
            ret = StateReturn(
                name = name, result = True,
                old_obj = exec["ret"], new_obj = {},
                comment = f"Public IP Address {public_ip_address_name} delete in progress."
            )
    except idemexc.NotFoundError:
        ret = StateReturn(
            name = name, result = True,
            comment = f"Public IP Address {public_ip_address_name} already absent."
        )

    return ret
