#!/usr/bin/env python3
"""
Read yaml, produce object
"""
from os import getcwd, listdir, path

import yaml
from cdktf import App
from logzero import logger

from common.policy import Approval, Eligibility  # pylint: disable=import-error
from common.terraform import TableItemStack  # pylint: disable=import-error


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
                        policies.append(policy_doc)

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


def intialise_policies(policy_documents, policy_path):
    """use policy dictionaries to intialise policy class objects.

    Args:
        policy_documents (list): _description_
        policy_path (str): _description_

    Returns:
        list: policy class objects
    """
    # policy_objects list to store initialised policy classes
    policy_objects = []
    # iterate through policy_documents to intialise policies
    for policy in policy_documents:

        policy["policy_path"] = policy_path
        # initialise object class based on policy type
        # fmt: off
        logger.info(
            "initialising policy: %s",
            policy["id"]
        )
        # fmt: on

        match policy["policy_type"]:
            case "eligibility":
                policy_objects.append(Eligibility(policy))
            case "approval":
                policy_objects.append(Approval(policy))
            case _:
                # fmt: off
                logger.error(
                    "type unkown: %s",
                    policy["policy_type"]
                )
                # fmt: on

    return policy_objects


def main():
    """Main entry point of the app"""
    # initialise terraform scope
    app = App()

    # construct path to policy directory
    policy_path = path.join(getcwd(), "policies")
    logger.info("policy path: %s", policy_path)

    # load individual policy documents as list of dicts
    policy_documents = load_policies_from_yaml(policy_path)

    # initialise list of Policy class objects
    policy_objects = intialise_policies(policy_documents, policy_path)

    # filter list of eliibility policies, because approval policies aren't
    # supported yet.
    # fmt: off
    elig_policies = [
        policy
        for policy in policy_objects
        if policy.policy_type == "eligibility"
    ]
    # fmt: on

    # initialise TableItemStack with the list of eligilbity policy objects.
    TableItemStack(
        app,
        "stack",
        elig_policies,
    )

    # synthesize terraform code
    app.synth()


if __name__ == "__main__":
    main()
