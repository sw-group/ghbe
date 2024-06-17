import connexion
import six
from werkzeug.exceptions import NotFound

from swagger_server.db.mongo_operations import MongoOperations
from swagger_server.models import StatisticsWorkflows
from swagger_server.models.repository import Repository  # noqa: E501
from swagger_server.models.statistics import Statistics  # noqa: E501

import swagger_server.db.mongo_db as db
from swagger_server.utils.util import generate_date_count_map, generate_label_count_map, \
    generate_metrics_workflow_map
from swagger_server.utils import mapper
from ..models import StatisticsPulls, StatisticsIssues, StatisticsRepositories


def get_comments_of_issue(owner, name, number, page=None):  # noqa: E501
    """Search issues of the repo by fullname

    Search issues of the repo by fullname # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str
    :param number: The number of the issue
    :type number: str
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int

    :rtype: List[Comment]
    """
    repo_full_name = f'{owner}/{name}'
    mongo_ops = MongoOperations(collection_name="comments")
    try:
        comments_data = mongo_ops.get_comments(repo=repo_full_name, number=number, page=page)
        comments = [
            mapper.map_response_to_comment(comment).to_dict()
            for comment in comments_data
        ]
        return comments, 200
    finally:
        mongo_ops.close()


def get_issues_of_repo(owner, name, issue_type, state=None, date_range=None, page=None, sort=None):  # noqa: E501
    """Search issues of the repo by fullname

    Search issues of the repo by fullname # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str
    :param issue_type: The type of the issues
    :type issue_type: str
    :param state: The state of the issues
    :type state: str
    :param date_range: Filter repositories by date range (e.g., 2023-01-01,2023-12-31)
    :type date_range: str
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int
    :param sort: Sort repositories by field in ascending or descending order
                (e.g., field-asc or field-desc).
                If order is not specified, default to ascending.
    :type sort: str

    :rtype: List[Issue]
    """

    repo_full_name = f'{owner}/{name}'
    mongo_ops = MongoOperations(collection_name=("issues" if issue_type == "issues" else "pullRequests"))
    try:
        issues_data = mongo_ops.get_issues(repo=repo_full_name, state=state, date_range=date_range, page=page,
                                           sort=sort)
        issues = [
            mapper.map_response_to_issue(issue).to_dict()
            for issue in issues_data
        ]
        return issues, 200
    finally:
        mongo_ops.close()


def get_repositories(name=None, language=None, is_private=None, date_range=None, stars=None, forks=None, issues=None,
                     pulls=None, workflows=None, page=None, sort=None):  # noqa: E501
    """Retrieve repositories with filtering options

    Retrieve repositories with filtering options # noqa: E501

    :param name: Filter repositories by name.
                 If providing a full name, prefix it with repo: (e.g., repo:owner/name).
    :type name: str
    :param language: Filter repositories by programming language
    :type language: str
    :param is_private: Filter private repositories
    :type is_private: bool
    :param date_range: Filter repositories by date range (e.g., 2023-01-01,2023-12-31)
    :type date_range: str
    :param stars: Filter repositories by stars range (e.g., 10,100)
    :type stars: str
    :param forks: Filter repositories by forks range (e.g., 5,50)
    :type forks: str
    :param issues: Filter repositories by issues range (e.g., 0,20)
    :type issues: str
    :param pulls: Filter repositories by pull requests range (e.g., 1,10)
    :type pulls: str
    :param workflows: Filter repositories by workflows range (e.g., 1,5)
    :type workflows: str
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int
    :param sort: Sort repositories by field in ascending or descending order
                (e.g., field-asc or field-desc). If order is not specified, default to ascending.
    :type sort: str

    :rtype: List[Repository]
    """

    mongo_ops = MongoOperations()
    try:
        repositories_data = mongo_ops.get_repositories(name=name, language=language, is_private=is_private,
                                                       date_range=date_range, stars=stars, forks=forks, issues=issues,
                                                       pulls=pulls, workflows=workflows, page=page, sort=sort)

        repositories = [
            mapper.map_response_to_repository(repo).to_dict()
            for repo in repositories_data
        ]
        return repositories, 200
    finally:
        mongo_ops.close()


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


def get_statistics_of_repository(owner, name, date_range):  # noqa: E501
    """Compute the statistics of a repository

    Compute the statistics of a repository # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str
    :param date_range: Filter repositories by date range (e.g., 2023-01-01,2023-12-31)
    :type date_range: str

    :rtype: Statistics
    """
    # Get issues and pulls data
    issues_data = {
        "OPEN": get_issues_of_repo(owner, name, "issues", "OPEN", date_range, -1)[0],
        "CLOSED": get_issues_of_repo(owner, name, "issues", "CLOSED", date_range, -1)[0]
    }
    pulls_data = {
        "OPEN": get_issues_of_repo(owner, name, "pulls", "OPEN", date_range, -1)[0],
        "CLOSED": get_issues_of_repo(owner, name, "pulls", "CLOSED", date_range, -1)[0],
        "MERGED": get_issues_of_repo(owner, name, "pulls", "MERGED", date_range, -1)[0]
    }

    # Compute statistics for issues
    stats_issues = StatisticsIssues(
        daily_closed_progress=generate_date_count_map(issues_data["CLOSED"]),
        daily_opened_progress=generate_date_count_map(issues_data["OPEN"])
    )

    # Compute statistics for pulls
    stats_pulls = StatisticsPulls(
        daily_closed_progress=generate_date_count_map(pulls_data["CLOSED"]),
        daily_opened_progress=generate_date_count_map(pulls_data["OPEN"]),
        merged=len(pulls_data["MERGED"])
    )

    # Combine issues and pulls data for repository statistics
    combined_issues = issues_data["OPEN"] + issues_data["CLOSED"] + \
                      pulls_data["OPEN"] + pulls_data["CLOSED"]

    # Compute statistics for repositories
    stats_repositories = StatisticsRepositories(
        stats=generate_label_count_map(combined_issues)
    )

    # Compute statistics for workflows
    workflows_data = get_workflows_of_repo(owner, name)[0]
    stats_workflows = StatisticsWorkflows(
        metrics=generate_metrics_workflow_map(workflows_data)
    )

    # Aggregate all statistics into a single object
    stats = Statistics(
        pulls=stats_pulls,
        issues=stats_issues,
        repositories=stats_repositories,
        workflows=stats_workflows
    )

    return stats.to_dict(), 200


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
    workflows = [
        mapper.map_response_to_workflow(workflow).to_dict()
        for workflow in workflows_from_db.get('workflows', [])
    ]

    return workflows, 200
