import mongomock
from flask_testing import TestCase
from swagger_server import create_app

class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup una volta per tutte le classi di test"""
        cls.mongo_client = mongomock.MongoClient()

    def create_app(self):
        """Required by Flask-Testing: return a Flask app instance"""
        app = create_app().app
        app.config['TESTING'] = True
        app.config['PROPAGATE_EXCEPTIONS'] = True
        app.mongo = self.mongo_client
        return app

    def assert_json_response(self, response, expected_status_code=200):
        """Helper to assert JSON response and status code"""
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.content_type, 'application/json')
        return response.get_json()
