#!/usr/bin/env python3
"""
Module Docstring
"""


import yaml
from logzero import logger


class Policy:
    """Base Class for policy objects."""

    def __init__(self, file_path):
        """Initialise client for identity store.

        Args:
            identity_store_id (string):
                The globally unique identifier for the identity store.
        """
        self.file_path = file_path
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
        logger.info("reading policy file: %s", self.file_path)

        with open(self.file_path, encoding="utf8") as stream:
            try:
                policy = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        logger.info("policy loaded successfully...")

        return policy
