import connexion
import six

from swagger_server.business import business
from swagger_server.models.metrics import Metrics  # noqa: E501

def get_metrics():  # noqa: E501
    """Get the metrics for filter configuration

    Get the metrics for filter configuration # noqa: E501


    :rtype: Metrics
    """
    return business.elaborate_metrics_repositories().to_dict()

