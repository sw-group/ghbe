#!/usr/bin/env python3
import json

import connexion
from connexion import problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse
from connexion.options import SwaggerUIOptions
from flask import jsonify

from swagger_server import encoder
from swagger_server.handler import exception

def main():
    options = SwaggerUIOptions(swagger_ui=True, swagger_ui_path="/ui")

    app = connexion.App(__name__, specification_dir='./swagger/', swagger_ui_options=options)
    app.app.json_encoder = encoder.JSONEncoder

    app.add_api('swagger.yaml',
                arguments={'title': 'Mining GitHub'},
                pythonic_params=True,
                swagger_ui_options=options)

    app.add_error_handler(404, exception.not_found)

    app.run(port=8080)


if __name__ == '__main__':
    main()
