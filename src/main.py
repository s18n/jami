#!/usr/bin/env python3
"""
Read yaml, produce object
"""


from os import getcwd, listdir
from os.path import isfile, join

from logzero import logger

from common.policy import Policy  # pylint: disable=import-error


def main():
    """Main entry point of the app"""

    # initialise policy lists
    elig_data = []
    appr_data = []

    # fetch policy files
    path = getcwd()
    elig_path = f"{path}/policies/eligibility/"
    appr_path = f"{path}/policies/approval/"
    elig_files = [f for f in listdir(elig_path) if isfile(join(elig_path, f))]
    appr_files = [f for f in listdir(appr_path) if isfile(join(appr_path, f))]

    # collect approval policy filenames
    for file in appr_files:
        logger.info("fetch appr policy...")
        appr_data.append(Policy(f"{appr_path}{file}"))

    # print all appr policies
    print([policy.policy for policy in appr_data])

    # collect elgibility policy filenames
    for file in elig_files:
        elig_data.append(Policy(f"{elig_path}{file}"))

    # print all elig policies
    print([policy.policy for policy in elig_data])


if __name__ == "__main__":
    main()
