#!/usr/bin/env python3
"""
Read yaml, produce object
"""
from os import getcwd, listdir, path

import yaml
from logzero import logger

from common.policy import Approval, Eligibility  # pylint: disable=import-error


def load_policies_from_yaml(policy_path):
    """function to load policy files from local policy directory & initialise
    as class objects.

    Args:
        policy_path (str): absolute path to policy directory.

    Returns:
        list: policy object list.
    """
    # initialise empty list to populate with policy objects
    policies = []

    # list all files in policy folder
    for policy_file in listdir(policy_path):

        # only load ".yaml" files
        if policy_file.endswith(".yaml"):

            # open policy file
            try:
                with open(
                    path.join(policy_path, policy_file), "r", encoding="UTF-8"
                ) as file:

                    # load separate yaml documents
                    for policy_doc in yaml.safe_load_all(file):
                        policy_doc["policy_path"] = policy_path

                        # initialise object class based on policy type
                        # fmt: off
                        logger.info(
                            "initialising policy: %s",
                            policy_doc["id"]
                            )
                        # fmt: on

                        match policy_doc["policy_type"]:
                            case "eligibility":
                                policies.append(Eligibility(policy_doc))
                            case "approval":
                                policies.append(Approval(policy_doc))
                            case _:
                                # fmt: off
                                logger.error(
                                    "type unkown: %s",
                                    policy_doc["policy_type"]
                                )
                                # fmt: on
            except FileNotFoundError as error:
                # fmt: off
                logger.error(
                    "failed to load policy: %s\n%s",
                    policy_file,
                    error
                )
                # fmt: on

    # return list of policy objects
    return policies


def main():
    """Main entry point of the app"""
    policy_data = []

    # construct path to policy directory
    policy_path = path.join(getcwd(), "policies")
    logger.info("policy path: %s", policy_path)

    # load & initialise individual policy documents
    policy_data = load_policies_from_yaml(policy_path)

    items = [
        print(policy.table_item)
        for policy in policy_data
        if policy.policy_type == "eligibility"
    ]

    print(items)


if __name__ == "__main__":
    main()
