#!/usr/bin/env python3
"""
Module Docstring
"""
from os import path

import boto3
import botocore
from jinja2 import Template

org_client = boto3.client("organizations")
sso_client = boto3.client("sso-admin")


def generate_table_item(data):
    """
    This function uses policy object data to generate a DynamoDB ready table
        item using Jinja2 and local template files.

        Args:
            data (class): Policy class object.

        Returns:
            str: Rendered template json as string.
    """
    policy_file_name = data.policy_type + ".json.j2"
    template_file = path.join(data.policy_path, "schemas/", policy_file_name)

    with open(template_file, "r", encoding="UTF-8") as file:
        policy_template = file.read()

    template = Template(policy_template)

    return template.render(data.__dict__)


class Policy:  # pylint: disable=too-few-public-methods
    """policy base class"""

    def __init__(self, data):
        # policy metadata
        self.policy_type = data["policy_type"]
        self.policy_path = data["policy_path"]
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.data = data
        self.ticket_number = data["ticket_number"]


class Eligibility(Policy):  # pylint: disable=too-few-public-methods
    """

    Args:
        Policy (_type_): _description_
    """

    def __init__(self, data):
        # inherit base class properties
        super().__init__(data)

        # eligibility properties
        self.permission_sets = self._fetch_permissions(data["permissions"])
        self.duration = data["duration"]
        self.approval_required = data["approval_required"]
        self.accounts = self._fetch_accounts(data["accounts"])
        self.ous = data["ous"]
        self.table_item = generate_table_item(self)

    def _fetch_accounts(self, accounts):
        account_data = []

        for account in accounts:
            try:
                response = org_client.describe_account(AccountId=account)
                account_data.append(
                    {"name": response["Account"]["Name"], "id": account}
                )
            except botocore.exceptions.ClientError as error:
                raise error

        return account_data

    def _fetch_permissions(self, permission_sets):
        permission_data = []

        for permission_set in permission_sets:
            try:
                response = sso_client.describe_permission_set(
                    # [TODO: parameters from config file]
                    InstanceArn="arn:aws:sso:::instance/ssoins-7535a6236da922a7",  # pylint: disable=line-too-long # noqa: 501
                    PermissionSetArn=permission_set,
                )
                permission_data.append(
                    # fmt: off
                    {
                        "arn": permission_set,
                        "name": response["PermissionSet"]["Name"]
                    }
                    # fmt: on
                )
            except botocore.exceptions.ClientError as error:
                raise error

        return permission_data

    # [TODO: use class props to generate policy table item]


class Approval(Policy):  # pylint: disable=too-few-public-methods
    """

    Args:
        Policy (_type_): _description_
    """

    def __init__(self, data):
        super().__init__(data)
        self.type = data["type"]
        self.group_ids = data["group_ids"]

    # [TODO: use class props to generate policy table item]
