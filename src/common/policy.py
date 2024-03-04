#!/usr/bin/env python3
"""
Module Docstring
"""

import json
from jinja2 import Template
from os import path
from logzero import logger
import boto3


org_client = boto3.client('organizations')
sso_client = boto3.client('sso-admin')


class Policy:  # pylint: disable=too-few-public-methods
    """policy base class"""

    def __init__(self, data):
        self.data = data
        self.policy_path = data['policy_path']
        self.name = data["name"]
        self.id = data["id"]
        self.description = data["description"]

        self.accounts = self._fetch_accounts(data["accounts"])
        self.ous = data["ous"]

        self.policy_type = data["policy_type"]
        self.ticket_number = data["ticket_number"]
        self.table_item = self._generate_table_item()


    def _generate_table_item(self):
        policy_file_name = self.policy_type + ".json.j2"
        template_file = path.join(self.policy_path, "schemas/", policy_file_name)

        logger.debug(template_file)

        with open(template_file, 'r') as file:
            policy_template = file.read()

        template = Template(policy_template)


        return template.render(self.__dict__)


    def _fetch_accounts(self, accounts):
        account_data = []

        for account in accounts:
            try:
                response = org_client.describe_account(AccountId=account)
                account_data.append({
                    "name": response['Account']['Name'],
                    "id": account
                })
                    
            except Exception as error:
                logger.error(error)

        for account in account_data:
            print(account['id'])


        return account_data


class Eligibility(Policy):  # pylint: disable=too-few-public-methods
    """

    Args:
        Policy (_type_): _description_
    """
    def __init__(self, data):
        super().__init__(data)
        self.permissions = self.fetch_permissions(data["permissions"])
        self.duration = data["duration"]
        self.approval_required = data["approval_required"]
    

    def fetch_permissions(self, permission_sets):
        permission_data = {}

        for permission_set in permission_sets:
            try:
                response = sso_client.describe_permission_set(
                    InstanceArn='string',
                    PermissionSetArn='string'
                )
                permission_data[response['PermissionSet']['Name']] = permission_set
            except Exception as error:
                logger.error(error)

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
