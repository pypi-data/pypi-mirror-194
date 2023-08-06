import pkg_resources
import unittest

try:
    FCD_VERSION = pkg_resources.get_distribution("mgtoolkit").version
except pkg_resources.DistributionNotFound:
    FCD_VERSION = "dev"


def console_entry():
    """If come from console entry point"""


# !! The main function are only here for debug.`!!
if __name__ == '__main__':
    unittest.main()
