#!/usr/bin/env python3
"""
Read yaml, produce object
"""


from logzero import logger

from common.policy import Policy  # pylint: disable=import-error


def main():
    """Main entry point of the app"""
    logger.info("fetching policies...")

    eligibility = Policy("eligibility.yaml")

    logger.info("eligibility policies:\n\t%s", eligibility.policy)


if __name__ == "__main__":
    main()
