# coding: utf-8

from __future__ import absolute_import

from flask import json
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
