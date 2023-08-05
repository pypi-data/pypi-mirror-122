# -*- coding: utf-8 -*-
"""
Azure Resource Manager (AzureRM) Python SDK wrapper class.

Copyright (c) 2019-2020, EITR Technologies, LLC.
Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals
from operator import itemgetter
import importlib
from inspect import signature
import logging

import six
import sys
import os

# Import third party libs
try:
    from azure.identity import (
        AzureAuthorityHosts,
        ClientSecretCredential,
        DefaultAzureCredential,
        UsernamePasswordCredential
    )
    from azure.core.exceptions import AzureError

    # exceptions
    import azure.core.exceptions


    HAS_AZURE = True
except ImportError:
    HAS_AZURE = False

# Import plugin helpers
import idem_azure.helpers.exc as idemexc


log = logging.getLogger(__name__)


def __init__(hub):
    hub.tool.azure.API = _AzureApi(hub, 'azure')
    hub.tool.azure.API_CLIENTS = {}


class _AzureApi:
    _client_map = {
        "compute": "ComputeManagement",
        "containerregistry": "ContainerRegistryManagement",
        "containerinstance": "ContainerInstanceManagement",
        "authorization": "AuthorizationManagement",
        "dns": "DnsManagement",
        "storage": "StorageManagement",
        "managementlock": "ManagementLock",
        "monitor": "MonitorManagement",
        "network": "NetworkManagement",
        "policy": "Policy",
        "resource": "ResourceManagement",
        "resource_subscription": "Subscription",
        "subscription": "Subscription",
        "web": "WebSiteManagement",
        "keyvault": "KeyVaultManagement",
        "redis": "RedisManagement",
        "postgresql": "PostgreSQLManagement",
        "loganalytics": "LogAnalyticsManagement",
        "applicationinsights": "ApplicationInsightsManagement",
        "msi": "ManagedServiceIdentity",
    }


    def __init__(self, hub, resource_name: str, parent=None):
        self._hub = hub
        self._resources = {}
        self.api_resource = None
        self.name = resource_name
        self.parent = parent


    def __getattr__(self, attr: str):
        """
        Get existing or add to resources if not yet built.
        :param attr: The key of the resource to add/get.
        """
        if attr not in self._resources:
            self._hub.log.debug(f"creating api resource node for {attr}.")
            self._resources[attr] = _AzureApi(self._hub, attr, self)

        return self._resources[attr]


    def __call__(self, ctx, *args, **kwargs):
        """
        Returns a cloud resource (could be a client or callable API).
        :param ctx: A dict with the keys/values for the execution of the Idem
        run located in `hub.idem.RUNS[ctx['run_name']]`.
        :param args: Positional argument list.
        :param kwargs: Keyword arguments passed directly to Azure SDK apis.

        By calling an object of this class, you receive the relevant Azure
        cloud resource the object represents. The can be a management client
        or a callable API (which would take *args and **kwargs).
        """
        cp = self.call_path_string()
        self._hub.log.debug(f"Generating Azure SDK interface for {cp}")
        ret = self.build_call_resource(ctx, *args, **kwargs)
        if callable(ret):
            try:
                ret = ret(*args, **kwargs)
            except azure.core.exceptions.ResourceNotFoundError as a:
                raise idemexc.NotFoundError(str(a))
            except AzureError as a:
                if a.error.code in {
                    "NotFound", "ResourceGroupNotFound", "ResourceNotFound"
                }:
                    raise idemexc.NotFoundError(str(a))
                else:
                    raise

        return ret


    def call_path_string(self):
        """
        Returns a 'dotted-notagion' of the call path for this instance.
        """
        path = ""
        if self.parent is None:
            path = self.name
        else:
            path = self.parent.call_path_string() + "." + self.name

        return path


    def build_call_resource(self, ctx, *args, **kwargs):
        """
        Recursively builds all _AzureApi api resources.
        :param ctx: A dict with the keys/values for the execution of the Idem
        run located in `hub.idem.RUNS[ctx['run_name']]`.
        :param args: A list of positional arguments to pass, as needed based
        on Azure API signatures, to the ultimate request (API call).
        :type args: tuple
        :param kwargs: Named parameters as key/value pairs.
        :type kwargs: dict
        :return: The callable (func) Azure request (API call).
        :rtype: callable

        For example, a call such as:

            my_azureapi.resource.resources.resource_group.list(ctx, *args, **kwargs)

        would result in a the creation (if not already created) the necessary
        _AzureApi wrappers for each of the dotted notation entries (indirectly
        via __getattr__). As well, for each of those wrappers, this call will
        create the Azure client and API Resource that relate.
        """
        ret = self.api_resource

        if ret is None:
            # Terminate the recursion at the top of the call tree:
            # the top of the tree is the cloud api instance and has only
            # child callable services, therefore nothing to contribute.
            if self.parent is not None:
                # Build the parent api resource.
                resource = self.parent.build_call_resource(ctx, *args, **kwargs)

                if resource is None:
                    # This is a top level service (e.g., resource). Build and return
                    # the client build (i.e., the api client).
                    if self.api_resource is None:
                        ret = self.get_client(ctx, *args, **kwargs)
                        self.api_resource = ret
                else:
                    # This is a leaf or intermediate(callable). Check whether
                    # anything exists for this DAG node, otherwise pass on the
                    # parent api resource.
                    try:
                        ret = getattr(self.parent.api_resource, self.name)
                        self.api_resource = ret
                    except AttributeError:
                        # No such API resource at this level, just pass on
                        # the parent's.
                        ret = resource

        return ret


    def determine_auth(self, ctx, **kwargs):
        """
        Acquire Azure RM Credential (mgmt modules).
        :param ctx: A dict with the keys/values for the execution of the Idem
        run located in `hub.idem.RUNS[ctx['run_name']]`.
        :param kwargs: Named parameters as key/value pairs.
        :type kwargs: dict
        :return: Credentials for Azure SDK APIs.

        See https://azuresdkdocs.blob.core.windows.net/$web/python/azure-identity/1.6.0/azure.identity.html#azure.identity.DefaultAzureCredential

        or the latest version for details of credential args/kwargs options.
        """
        service_principal_cred_keys = {"client_id", "secret", "tenant"}
        user_pass_cred_keys = {"client_id", "username", "password"}

        if ctx.get("acct"):
           for key, val in ctx["acct"].items():
                # explicit kwargs override acct
                kwargs.setdefault(key, val)

        cred_kwargs = {}

        if 'authority' in kwargs:
            authority = getattr(AzureAuthorityHosts, kwargs["authority"])
        cred_kwargs.setdefault("authority", AzureAuthorityHosts.AZURE_PUBLIC_CLOUD)

        if service_principal_cred_keys.issubset(kwargs):
            if not (kwargs["client_id"] and
                    kwargs["secret"] and
                    kwargs["tenant"]):
                raise Exception(
                    "The client_id, secret, and tenant parameters must all be "
                    "populated if using service principals."
                )
            # cred_kwargs can include:
            #   authority: Authority of an Azure Active Directory endpoint
            #               default: login.microsoftonline.com
            credential = ClientSecretCredential(
                    kwargs["tenant"],
                    kwargs["client_id"],
                    kwargs["secret"],
                    **cred_kwargs)
        elif user_pass_cred_keys.issubset(kwargs):
            if not (kwargs["username"] and
                    kwargs["password"] and
                    kwargs["client_id"]):
                raise Exception(
                    "Not all of required username, password and client_id in "
                    "acct profile and for username/password authentication."
                )
            # cred_kwargs can include:
            #   authority: Authority of an Azure Active Directory endpoint
            #               default: login.microsoftonline.com
            #   tenant_id: tenant ID or domain associated with a tenant
            #               default: ‘organizations’ tenant (not great)
            #   cache_persistence_options: TokenCachePersistenceOptions dict
            credential = UsernamePasswordCredential(
                kwargs["client_id"],
                kwargs["username"],
                kwargs["password"],
                **cred_kwargs
            )
        else:
            raise Exception(
                "Unable to determine credentials. "
                "A subscription_id with username and password, "
                "or client_id, secret, and tenant or a profile with the "
                "required parameters populated"
            )

        if "subscription_id" not in kwargs:
            raise Exception("A subscription_id must be specified")

        return credential, kwargs["subscription_id"]


    def get_client(self, ctx, *args, **kwargs):
        """
        Dynamically load and return a management client object.

        :param ctx: A dict with the keys/values for the execution of the Idem
        run located in `hub.idem.RUNS[ctx['run_name']]`.
        :param args: Positional argument list.
        type args: tuple
        :param kwargs: Keyword arguments passed directly to Azure SDK apis.
        :type kwargs: dict
        :return: Azure ManagementClient instance.
         """
        map_value = _AzureApi._client_map[self.name]
        if map_value is None:
            # No client for this node, short circuit return.
            return None

        # if client_type in ["policy", "resource_subscription"]:
        #     module_name = "resource"
        # elif client_type in ["managementlock"]:
        #     module_name = "resource.locks"
        # elif client_type in ["postgresql"]:
        #     module_name = "rdbms.postgresql"
        # else:
        #     module_name = client_type

        try:
            client_module = importlib.import_module("azure.mgmt." + self.name)
            # pylint: disable=invalid-name
            Client = getattr(client_module, "{0}Client".format(map_value))
        except ImportError:
            raise sys.exit("The azure {0} client is not available.".format(self.name))

        try:
            (
                credential,
                subscription_id
            ) = self.determine_auth(ctx, **kwargs)
        except Exception as exc:
            raise sys.exit(exc)

        if "subscription" in self.name:
            client = Client(credential=credential)
        else:
            client = Client(
                credential=credential,
                subscription_id=subscription_id)

        # TODO: add user agent info for user debugging
        #client.config.add_user_agent("idem-azure")

        return client
