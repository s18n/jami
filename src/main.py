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
    logger.info("fetching policies...")

    path = getcwd()
    elig_data = []
    elig_path = f"{path}/policies/eligibility/"
    print(listdir(elig_path))
    elig_files = [f for f in listdir(elig_path) if isfile(join(elig_path, f))]

    # collect elgibility policy filenames
    for file in elig_files:
        print(file)
        elig_data.append(Policy(f"{elig_path}{file}"))

    # print eligibility policies
    for policy in elig_data:
        print(f"file_path:\n\t{policy.file_path}")
        print(f"policy:\n\t{policy.policy}")

    # eligibility = Policy("eligibility.yaml")
    # approval = Policy("approval.yaml")

    # logger.info("eligibility policies:\n\t%s", eligibility.policy)
    # logger.info("approval policies:\n\t%s", approval.policy)


if __name__ == "__main__":
    main()
