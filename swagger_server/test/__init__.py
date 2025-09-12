from unittest.mock import patch

from flask_testing import TestCase
from mongomock import MongoClient

from swagger_server import create_app


class PyMongoMock(MongoClient):
    """Mock compatibile con PyMongo che usa mongomock sotto"""

    def __init__(self):
        super().__init__()
        # usa un db fittizio "testdb"
        self.db = self.client["test"]

    def init_app(self, app):
        # Non fa nulla nei test, serve solo per compatibilità
        return self


class BaseTestCase(TestCase):

    def create_app(self):
        # Patch del global `mongo` usato da tutto il codice
        patcher = patch("swagger_server.db.database.mongo", new_callable=PyMongoMock)
        self.addCleanup(patcher.stop)
        self.mongo = patcher.start()

        """Required by Flask-Testing: return a Flask app instance"""
        app = create_app().app
        app.config['TESTING'] = True
        app.config['PROPAGATE_EXCEPTIONS'] = True
        return app

    def assert_json_response(self, response, expected_status_code=200):
        """Helper to assert JSON response and status code"""
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.content_type, 'application/json')
        return response.get_json()
