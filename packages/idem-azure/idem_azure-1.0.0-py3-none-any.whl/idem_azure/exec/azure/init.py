# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management exec module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

This file implements the vast majority of the Plugin Oriented Programming
(POP) exec Sub.

The basic operating model is building Subs as needed to match the nature of a
call to an exec. For example, a call like:

    hub.exec.azure.compute.virtual_machines.list(ctx, ...)

will work, even though no exec subdirectories exist to match that call path.
Instead, the classes herein dynamically build the POP Subs to match and tie
them to the appropriate Azure Python SDK wrappers within the tool Sub of this
project.
"""

from inspect import signature

from azure.core.exceptions import AzureError

from pop.loader import LoadedMod
from pop.hub import Sub

# Import plugin helpers
import idem_azure.helpers.exc as idemexc


def __init__(hub):
    hub.exec.azure.ACCT = ["azure"]
    hub.exec.azure.OBJECT_CACHE = {}
    hub.exec.azure._subs = ClientSubs(hub)


class _SubDict(dict[str, Sub]):
    """
    This class creates a dict to dynamically add Subs as sets.

    The point is to allow a developer to make a call to any 'purportedly'
    valid Azure API without worrying that it is discovered a priori to the
    call. For example, calling on:

        hub.exec.azure.compute.virtual_machines.list(...)

    and later

        hub.exec.azure.compute.virtual_machines.get(...)

    requires the creation a DAG of Subs representing each attribute
    of the call paths.

    This class is the dict that allows the devleoper to write the callpath,
    fully assuming the call path DAG will get created as needed.
    """
    def __init__(self, hub):
        super()
        self._hub = hub

    def __contains__(self, item: str):
        """Always accept keys because all API calls get dynamically built."""
        return True

    def __missing__(self, item: str):
        """
        Generate the missing key/value pairs as needed.
        :param: item: The key of the (as yet) missing value.

        Subclasses must implement the _missing method, to which this method
        defers.
        """
        return self._missing(item)

    def _missing(self, item: str):
        """
        Create missing key/value pairs. Force subclasses to implement.
        :param: item: The key of the missing value to be added).
        """
        raise KeyError

    def __getattr__(self, item: str):
        """
        Support attribute requests on subclasses.
        :param item: The name (key) of the item to retrieve (or add).
        """
        return self[item]

    def __getattribute__(self, item: str):
        """
        Support attributes via '.' notation -- needed to cover for 'get'.
        """
        if item == "get":
            return self.__getattr__(item)
        else:
            return super().__getattribute__(item)


class ClientSubs(_SubDict):
    """
    This class represents the Azure Management layer. Each Azure SDK
    Management Client maps to a topic, such as "compute", "network", etc.).
    For each of those topics, there are many undelrying API sets.

    For example, when calling an Azure Management Client API, the developer
    can call:

        hub.exec.azure.compute.virtual_machines.list(...)

    or the like.

    This particular class creates the DAG of Subs representing all
    such calls to ManagementClient and underlying API sets.
    """
    def __init__(self, hub):
        """
        Initializes the class.
        :param hub: The redistributed pop central hub to which to attach
        the Subs created by this class.
        """
        super().__init__(hub)
        self.sub = self._hub.exec.azure

    def _missing(self, client_name: str):
        """
        Return the Sub representing the management client.
        :param client_name: The name of the client as represented in the tool
        Sub (i.e., hub.tool.azure.init) _AzureAPI._client_map. For example,
        to call ComputeManagementClient APIs, client_name should contain
        "compute" as its value.
        """
        azure_api = getattr(self._hub.tool.azure.API, client_name)
        sub = Sub(hub=self._hub, subname=client_name, root=self.sub, init=False)
        sub._subs = ClientSub(self._hub, sub, azure_api)
        self[client_name] = sub
        return sub._subs


class ClientSub(_SubDict):
    """
    Generates a Sub to represent Azure ...ManagementClient classes, for
    example ComputeManagementClient.

    This class implements the _subs dict of the Sub representing a
    particuler MangementClient.
    """
    def __init__(self, hub, sub: Sub, client_azure_api):
        """
        Initialize the instance.
        :param hub: The redistributed pop central hub to which to attach
        the Subs created by this class.
        :param sub: The parent Sub of this Sub.
        :param client_azure_api: The client _AzureApi object )
        """
        super().__init__(hub)
        self.sub = sub
        self._client_azure_api = client_azure_api

    def _missing(self, api_name: str) -> Sub:
        """
        Return the Sub representing the ManagementClient API set.
        :param api_name: The name of the API set within the ManagementClient.
        For example, "virtual_machines" (i.e., from ComputeManagementClient).
        """
        azure_api = getattr(self._client_azure_api, api_name)
        sub = Sub(hub=self._hub, subname=api_name, root=self.sub, init=False)
        sub._subs = ApiSub(self._hub, sub, azure_api)
        self[api_name] = sub
        return sub._subs


class ApiSub(_SubDict):
    """
    Generates a Sub to represent the methods of an Azure ...ManagementClient
    API set.

    For example, virtual_machines.??? in the ComputeManagementClient.

    This class implements the _subs dict of the Sub representing the
    available methods within a MangementClient.
    """
    def __init__(self, hub, sub: Sub, azure_api):
        """
        Initialize the instance.
        :param hub: The redistributed pop central hub to which to attach
        the Subs created by this class.
        :param sub: The parent Sub of this Sub.
        :param azure_api: The API set _AzureApi object (from the tool Sub).
        """
        super().__init__(hub)
        self.sub = sub
        self.azure_api = azure_api

    def _missing(self, api_name: str) -> "ContractMod":
        """
        Return the Sub representing a single method within the API set.
        :param api_name: The name of the method within an API set from
        a ManagementClient. For example, "list" for making a call to
        ComputeManagementClient.virtual_machines.list.
        """
        azure_method = getattr(self.azure_api, api_name)
        self[api_name] = ContractMod(self._hub, azure_method)
        return self[api_name]


class ContractMod(LoadedMod):
    """
    A Sub (class) to represent actually callable methods within Azure
    ...ManagementClient API sets.

    For example, "list" within the virtual_machines API set in
    ComputeManagementClient.
    """
    def __init__(self, hub, azure_method):
        """
        Initialize the instance.
        :param hub: The redistributed pop central hub to which to attach
        the Subs created by this class.
        :param azure_method: The _AzureApi representing the method (from the
        tool Sub).
        """
        super().__init__(name=azure_method.name)
        self._hub = hub
        self._azure_method = azure_method

    @property
    def signature(self):
        """
        Returns the signature of the the __call__ method.

        When calling functions that contain "ctx" within the arguments to the
        function, POP injects the acct profile into "ctx" so it needs the
        call signature in order to do that.
        """
        return signature(self.__call__)

    def _missing(self, item: str):
        """Return a value for the given key (item)."""
        return self

    async def __call__(self, ctx, *args, **kwargs):
        """
        Closure on hub/target that calls the target function.
        :param ctx: A dict with the keys/values for the execution of the Idem run
        located in `hub.idem.RUNS[ctx['run_name']]`.
        :param args: Tuple of positional arguments.
        :param kwargs: dict of named *keyward/value) arguments.
        :return: Results of call in standard exec packaging:
            result: True if the API succeeded, False otherwise.
            ret: Any data returned by the API.
            comment: Any relevant info generated by the API (e.g.,
            "code 200", "code 404", an exception message, etc.).
        """
        ret = {"result": False, "ret": None, "comment": ""}
        res = self._azure_method(ctx, *args, **kwargs)

        # TODO: fix this so recursive_contracts works instead.
        if hasattr(self._hub, "SUBPARSER") and  self._hub.SUBPARSER == "exec":
            # Convert any core ItemPaged to a list.
            res = self._hub.tool.azure.utils.paged_object_to_list(res)
        # everything will always just work with dicts.
        if hasattr(res, "as_dict"):
            res = res.as_dict()

        ret["ret"] = res
        ret["result"] = True

        return ret
