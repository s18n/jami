#!/usr/bin/env python3
"""
Module Docstring
"""


class Policy:  # pylint: disable=too-few-public-methods
    """policy base class"""

    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        self.description = data["description"]

        self.accounts = data["accounts"]
        self.ous = data["ous"]

        self.policy_type = data["policy_type"]
        self.ticket_number = data["ticket_number"]


class Eligibility(Policy):  # pylint: disable=too-few-public-methods
    """

    Args:
        Policy (_type_): _description_
    """

    def __init__(self, data):
        super().__init__(data)
        self.permissions = data["permissions"]
        self.duration = data["duration"]
        self.approval_required = data["approval_required"]


class Approval(Policy):  # pylint: disable=too-few-public-methods
    """

    Args:
        Policy (_type_): _description_
    """

    def __init__(self, data):
        super().__init__(data)
        self.type = data["type"]
        self.group_ids = data["group_ids"]
