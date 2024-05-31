import json

import connexion
import six
from werkzeug.exceptions import NotFound

from swagger_server.models import repository
from swagger_server.models.issue import Issue  # noqa: E501
from swagger_server.models.repository import Repository  # noqa: E501
from swagger_server.models.statistics import Statistics  # noqa: E501
from swagger_server.models.workflow import Workflow  # noqa: E501
from swagger_server import util
import swagger_server.db.mongo_db as db
from swagger_server.utils import mapper


def get_issues_of_repo(owner, name, type=None, _is=None, date_range=None, page=None, sort=None):  # noqa: E501
    """Search issues of the repo by fullname

    Search issues of the repo by fullname # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str
    :param type: The type of the issues
    :type type: str
    :param _is: The state of the issues
    :type _is: str
    :param date_range: Filter repositories by date range (e.g., \&quot;2023-01-01,2023-12-31\&quot;)
    :type date_range: str
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int
    :param sort: Sort repositories by field in ascending or descending order (e.g., \&quot;field-asc\&quot; or \&quot;field-desc\&quot;). If order is not specified, default to ascending. 
    :type sort: str

    :rtype: List[Issue]
    """
    return 'do some magic!'


def get_repositories(name=None, language=None, is_private=None, date_range=None, stars=None, forks=None, issues=None, pulls=None, workflows=None, page=None, sort=None):  # noqa: E501
    """Retrieve repositories with filtering options

    Retrieve repositories with filtering options # noqa: E501

    :param name: Filter repositories by name. If providing a full name, prefix it with \&quot;repo:\&quot; (e.g., \&quot;repo:owner/name\&quot;). 
    :type name: str
    :param language: Filter repositories by programming language
    :type language: str
    :param is_private: Filter private repositories
    :type is_private: bool
    :param date_range: Filter repositories by date range (e.g., \&quot;2023-01-01,2023-12-31\&quot;)
    :type date_range: str
    :param stars: Filter repositories by stars range (e.g., \&quot;10,100\&quot;)
    :type stars: str
    :param forks: Filter repositories by forks range (e.g., \&quot;5,50\&quot;)
    :type forks: str
    :param issues: Filter repositories by issues range (e.g., \&quot;0,20\&quot;)
    :type issues: str
    :param pulls: Filter repositories by pull requests range (e.g., \&quot;1,10\&quot;)
    :type pulls: str
    :param workflows: Filter repositories by workflows range (e.g., \&quot;1,5\&quot;)
    :type workflows: str
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int
    :param sort: Sort repositories by field in ascending or descending order (e.g., \&quot;field-asc\&quot; or \&quot;field-desc\&quot;). If order is not specified, default to ascending. 
    :type sort: str

    :rtype: List[Repository]
    """

    return 'do some magic!'


def get_repository_by_full_name(owner, name):  # noqa: E501
    """Search repositories by filter

    Search repositories by filter # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str

    :rtype: Repository
    """
    repo_full_name = f"{owner}/{name}"

    # find the repo into db and get it
    repo = db.get_repository_by_id(repo_full_name)

    if repo is None:
        raise NotFound

    # map the json into Repository model
    r = mapper.map_response_to_repository(repo)
    return r.to_dict(), 200


def get_statistics_of_repository(owner, name, date_range=None):  # noqa: E501
    """Compute the statistics of a repository

    Compute the statistics of a repository # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str
    :param date_range: Filter repositories by date range (e.g., \&quot;2023-01-01,2023-12-31\&quot;)
    :type date_range: str

    :rtype: Statistics
    """
    return 'do some magic!'


def get_workflows_of_repo(owner, name):  # noqa: E501
    """Search workflows of the repo by fullname

    Search workflows of the repo by fullname # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str

    :rtype: List[Workflow]
    """
    repo_full_name = f"{owner}/{name}"

    if not db.exist_repository(repo_full_name):
        raise NotFound

    workflows_from_db = db.get_repository_workflow(repo_full_name)

    # List to store Workflow instances
    workflows = []

    # Print each workflow
    for workflow in workflows_from_db.get('workflows', []):
        workflows.append(mapper.map_response_to_workflow(workflow).to_dict())

    return workflows, 200
