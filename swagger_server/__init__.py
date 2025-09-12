import connexion
from flask import jsonify
from werkzeug.exceptions import HTTPException

import swagger_server.db.database
from swagger_server.controllers.gui_controller import register_gui_routes
from swagger_server.controllers.repository_controller import register_repository_routes
from swagger_server.encoder import JSONEncoder


def create_app():
    # Create the connexion app
    connex_app = connexion.App(__name__, specification_dir='./swagger')
    connex_app.app.json_encoder = JSONEncoder

    connex_app.app.config['MONGO_URI'] = "mongodb://localhost:27017/mining"
    swagger_server.db.database.mongo.init_app(connex_app.app)

    # Load API from swagger.yaml
    connex_app.add_api(
        'swagger.yaml',
        arguments={'title': 'Mining GitHub'},
        pythonic_params=True
    )

    # Global error handler for JSON responses
    @connex_app.app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description
        }).data
        response.content_type = "application/json"
        return response

    # Register the extra Flask route
    register_gui_routes(connex_app.app)
    register_repository_routes(connex_app.app)

    return connex_app  # return the Flask app, not the Connexion wrapper
