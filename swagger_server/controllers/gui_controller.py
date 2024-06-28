import connexion
import six

from swagger_server.db.mongo_operations import MongoOperations
from swagger_server.models.metrics import Metrics  # noqa: E501
from swagger_server import util
from swagger_server.utils.util import process_repositories


def get_metrics():  # noqa: E501
    """Get the metrics for filter configuration

    Get the metrics for filter configuration # noqa: E501


    :rtype: Metrics
    """
    mongo_ops = MongoOperations()
    repositories_list = mongo_ops.get_repositories(page=-1)

    # Process the repositories
    metrics = process_repositories(repositories_list)
    return metrics, 200

