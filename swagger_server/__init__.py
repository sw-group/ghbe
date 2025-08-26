import connexion
from flask_cors import CORS

from swagger_server.controllers.gui_controller import register_routes
from swagger_server.encoder import JSONEncoder

def create_app():
    # Create the connexion app
    connex_app = connexion.App(__name__, specification_dir='./swagger')
    connex_app.app.json_encoder = JSONEncoder

    # Enable CORS on the underlying Flask app
    CORS(connex_app.app, resources={r"*": {"origins": "*"}})

    # Load API from swagger.yaml
    connex_app.add_api(
        'swagger.yaml',
        arguments={'title': 'Mining GitHub'},
        pythonic_params=True
    )

    # Register the extra Flask route
    register_routes(connex_app.app)

    return connex_app  # return the Flask app, not the Connexion wrapper
