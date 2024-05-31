from connexion import problem
from connexion.lifecycle import ConnexionRequest, ConnexionResponse

def not_found(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
    return problem(
        title="NotFound",
        detail="The requested resource was not found on the server",
        status=404,
    )