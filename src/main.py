#!/usr/bin/env python3
"""
Read config, produce object
"""

import os

import yaml
from logzero import logger

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


def read_policy(policy_file):
    """Read yaml file from policy directory

    Args:
        policy_file (string): Policy yaml file name.

    Returns:
        dict: Policy object.
    """
    # get current directory
    path = os.getcwd()

    logger.info("reading policy file...")
    with open(f"{path}/policies/{policy_file}", encoding="utf8") as stream:
        try:
            policy = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    logger.info("policy loaded successfully...")
    return policy


def main():
    """Main entry point of the app"""
    logger.info("fetching policies...")
    eligibility = read_policy("eligibility.yaml")
    approval = read_policy("approval.yaml")

    logger.info("approval policies:\n\t%s", approval)
    logger.info("eligibility policies:\n\t%s", eligibility)


if __name__ == "__main__":
    main()
