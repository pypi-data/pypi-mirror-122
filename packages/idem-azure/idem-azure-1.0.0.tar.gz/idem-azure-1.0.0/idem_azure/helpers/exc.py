# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management exceptions module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""

class NotFoundError(Exception):
    """Exception raised for resources not found in Azure."""

    def __init__(self, message: str):
        """
        Initialize an instance of this class.
        :param message: String message to present when rendering the exception.
        """
        self.message = message
        super().__init__(self.message)
