"""
    Ory APIs

    Documentation for all public and administrative Ory APIs. Administrative APIs can only be accessed with a valid Personal Access Token. Public APIs are mostly used in browsers.   # noqa: E501

    The version of the OpenAPI document: v1.1.19
    Contact: support@ory.sh
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ory_client
from ory_client.model.null_plan import NullPlan
globals()['NullPlan'] = NullPlan
from ory_client.model.subscription import Subscription


class TestSubscription(unittest.TestCase):
    """Subscription unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSubscription(self):
        """Test Subscription"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Subscription()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
