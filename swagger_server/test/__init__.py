import logging

import connexion
from flask_testing import TestCase

from swagger_server import encoder


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = encoder.JSONEncoder
        app.add_api('swagger.yaml')
        return app.app
