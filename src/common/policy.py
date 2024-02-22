#!/usr/bin/env python3
"""
Module Docstring
"""


import os

import yaml
from logzero import logger


class Policy:
    """Base Class for policy objects."""

    def __init__(self, file_name):
        """Initialise client for identity store.

        Args:
            identity_store_id (string):
                The globally unique identifier for the identity store.
        """
        self.file_name = file_name
        self.policy = self.read()

    def update(self):
        """Add meta data to policy object.

        Args:
            bar (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.policy

    def read(self):
        """Read policy file.

        Returns:
            _type_: _description_
        """
        # get current directory
        path = os.getcwd()

        logger.info("reading policy file: %s", self.file_name)

        policy_file_path = f"{path}/policies/{self.file_name}"
        with open(policy_file_path, encoding="utf8") as stream:
            try:
                policy = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        logger.info("policy loaded successfully...")

        return policy
