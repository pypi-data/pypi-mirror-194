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
from ory_client.model.identity import Identity
from ory_client.model.session import Session
globals()['Identity'] = Identity
globals()['Session'] = Session
from ory_client.model.successful_native_registration import SuccessfulNativeRegistration


class TestSuccessfulNativeRegistration(unittest.TestCase):
    """SuccessfulNativeRegistration unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSuccessfulNativeRegistration(self):
        """Test SuccessfulNativeRegistration"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SuccessfulNativeRegistration()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
