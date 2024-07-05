# coding: utf-8

from flask import Flask, json
from six import BytesIO
from swagger_server.test import BaseTestCase
from swagger_server.models.metrics import Metrics  # Adjust path if necessary

class TestGuiController(BaseTestCase):
    """GuiController integration test stubs"""

    def test_get_metrics(self):
        """Test case for get_metrics

        Get the metrics for filter configuration
        """
        response = self.client.get('/ghbe/api/v1/metrics')
        self.assert200(response, 'Response body is : ' + response.data.decode('utf-8'))

# No need for `if __name__ == '__main__':` block when using pytest


'''
# coding: utf-8

from __future__ import absolute_import

from flask import Flask, json
from six import BytesIO

from swagger_server.models.metrics import Metrics  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGuiController(BaseTestCase):
    """GuiController integration test stubs"""

    def test_get_metrics(self):
        """Test case for get_metrics

        Get the metrics for filter configuration
        """
        response = self.client.open(
            '/ghbe/api/v1/metrics',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()



if __name__ == '__main__':
    import unittest
    unittest.main()
'''