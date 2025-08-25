import connexion
from flask_cors import CORS

from swagger_server import encoder


def create_app():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder

    CORS(app.app, resources={r"*": {"origins": "*"}})

    app.add_api('swagger.yaml', arguments={'title': 'Mining GitHub'}, pythonic_params=True)

    return app