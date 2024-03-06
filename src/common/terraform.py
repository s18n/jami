#!/usr/bin/env python3
"""
Module Docstring
"""
from cdktf import TerraformStack
from constructs import Construct

# fmt: off
from imports.aws.dynamodb_table_item import \
    DynamodbTableItem  # pylint: disable=import-error
# fmt: on
from imports.aws.provider import AwsProvider  # pylint: disable=import-error


class DdbTableItem(Construct):
    """dynamodb table item

    Args:
        Construct (_type_): _description_
    """

    def __init__(self, scope: Construct, name: str, data):
        super().__init__(scope, name)

        self.table_item = DynamodbTableItem(
            self,
            "example_1",
            hash_key="1234567",
            item=data.table_item,
            table_name="item",
        )


class TableItemStack(TerraformStack):
    """table item stack

    Args:
        TerraformStack (_type_): _description_
    """

    def __init__(self, scope: Construct, name: str, policies: list):
        super().__init__(scope, name)

        AwsProvider(self, "aws", region="eu-west-2")

        self.policies = self.init_table_items(policies)

    def init_table_items(self, policies: list):
        """initialise table item objects.

        Args:
            policies (list): _description_

        Returns:
            _type_: _description_
        """
        policy_objects = []
        for policy in policies:
            policy_objects.append(DdbTableItem(self, policy.name, policy))
        return policy_objects
