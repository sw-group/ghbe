import logging
import os

import connexion
from flask_testing import TestCase

from swagger_server import create_app

class BaseTestCase(TestCase):
    """Base test case for all integration tests"""

    def create_app(self):
        """Return the Flask app to be tested"""
        self.app = create_app().app
        self.app.config['TESTING'] = True
        return self.app

    def assertJsonResponse(self, response, expected_status_code=200):
        """Helper to assert JSON response and status code"""
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.content_type, 'application/json')
        return response.get_json()
