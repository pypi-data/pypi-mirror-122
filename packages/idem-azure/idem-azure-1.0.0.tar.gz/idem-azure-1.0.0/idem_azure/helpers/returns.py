# -*- coding: utf-8 -*-
"""
Azure Resource Manager (ARM) Management exceptions module.

Copyright (c) 2021 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
"""


class StateReturn(dict):
    """
    Convenience class to manage POP state returns.
    """
    def __init__(self,
        name = None, result = None, comment = None,
        old_obj = None, new_obj = None
    ):
        """
        Initialize an object of this class.
        :param name: The name of the state (e.g. from a SLS file).
        :param result: True if the state call works, False otherwise.
        :param comment: Any relevant comments to the state execution.
        For example a 200 code from an HTTP call or a mere readable comment.
        :param old_obj: For state changes, the object's state
        (e.g., dict of values).
        prior to any state change request executions.
        :param new_obj: For state changes, the new object's state after any
        state change equest executions.
        """
        super(StateReturn, self).__init__([
            ("name", name),
            ("result", result),
            ("comment", comment),
            ("changes", {})
        ])
        if old_obj or new_obj:
            self['changes'] = {
                "old": old_obj,
                "new": new_obj
            }
