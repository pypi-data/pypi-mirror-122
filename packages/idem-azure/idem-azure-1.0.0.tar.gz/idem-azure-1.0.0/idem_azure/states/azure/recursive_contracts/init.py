# -*- coding: utf-8 -*-
"""
Azure Resource Manager (AzureRM) state contracts.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

from idem_azure.helpers.returns import StateReturn
from idem_azure.helpers.log import entry_exit_log


@entry_exit_log
def pre(hub, ctx):
    kwargs = ctx.get_arguments()
    if "ctx" in kwargs:
        assert (
            kwargs["ctx"].acct
        ), f"No credentials found for profile: {hub.OPT.acct.get('acct_profile')}"


@entry_exit_log
async def call(hub, ctx):
    # State calls are always state(hub, ctx, name, ...)
    if "name" in ctx.kwargs:
        name = ctx.kwargs['name']
    elif len(ctx.args) >2 :
        name = ctx.args[2]
    else:
        name = "<unknown>"

    try:
        ret = await ctx.func(*ctx.args, **ctx.kwargs)
    except Exception as e:
        ret = StateReturn(
            name = name, result = False, comment = e.__str__()
        )

    return ret


@entry_exit_log
def post(hub, ctx):
    pass
