"""This module is about testing the logger."""

import sys

from unittest import TestCase

LOGGER = sys.modules["Rainmeter.logger"]


class TestFunctions(TestCase):
    """Test class wrapper using unittest."""

    # pylint: disable=W0703; This is acceptable since we are testing it not failing

    def test_info(self):
        """Info should not through exceptions due to settings."""
        try:
            LOGGER.info("info test")
        except Exception as error:
            self.fail("logger.info() raised exception '" + str(error) + "'")

    def test_error(self):
        """Error should not through exception due to settings."""
        try:
            LOGGER.error("error test")
        except Exception as error:
            self.fail("logger.error() raised exception '" + str(error) + "'")
