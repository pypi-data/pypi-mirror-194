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
from ory_client.model.identity_state import IdentityState
from ory_client.model.identity_with_credentials import IdentityWithCredentials
globals()['IdentityState'] = IdentityState
globals()['IdentityWithCredentials'] = IdentityWithCredentials
from ory_client.model.update_identity_body import UpdateIdentityBody


class TestUpdateIdentityBody(unittest.TestCase):
    """UpdateIdentityBody unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdateIdentityBody(self):
        """Test UpdateIdentityBody"""
        # FIXME: construct object with mandatory attributes with example values
        # model = UpdateIdentityBody()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
