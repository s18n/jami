#!/usr/bin/env python3
"""
Read config, produce object
"""

from logzero import logger

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    """Main entry point of the app"""
    logger.debug("hello")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    print("hello world")


if __name__ == "__main__":
    main()
