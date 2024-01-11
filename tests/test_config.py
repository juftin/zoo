"""
Congiguration tests
"""

import logging

from zoo.config import ZooSettings


def test_rich_logging() -> None:
    """
    Test rich logging
    """
    logger = logging.getLogger("test_rich_logging")
    assert logger.handlers == []
    ZooSettings.rich_logging([logger])
    assert len(logger.handlers) == 1


def test_rich_logging_string() -> None:
    """
    Test rich logging with string
    """
    logger = logging.getLogger("test_rich_logging_string")
    assert logger.handlers == []
    ZooSettings.rich_logging(["test_rich_logging_string"])
    assert len(logger.handlers) == 1
