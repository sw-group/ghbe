from flask import jsonify
from werkzeug.exceptions import NotFound

import swagger_server.db.mongo_db as db
from swagger_server.business import business
from swagger_server.db.mongo_operations import MongoOperations
from swagger_server.models import RepositoriesList, IssuesList
from swagger_server.models.repository import Repository  # noqa: E501
from swagger_server.models.statistics import Statistics  # noqa: E501
from swagger_server.utils import mapper
from swagger_server.utils.util import generate_date_count_map, generate_label_count_map, \
    generate_metrics_workflow_map, accumulate_stats, validate_date_range
from swagger_server.models import StatisticsIssues, StatisticsPulls, StatisticsRepositories, StatisticsWorkflows
from typing import Tuple


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

    :rtype: CommentsList
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
    :param sort: Sort repositories by field in ascending or descending order  (e.g., field-asc or field-desc). If order is not specified, default to ascending. 
    :type sort: str

    :rtype: IssuesList
    """

    repo_full_name = f'{owner}/{name}'
    return business.elaborate_issues(repo_full_name, issue_type, state, date_range, page, sort).to_dict()


def get_repositories(name=None, language=None, is_private=None, date_range=None, stars=None, forks=None, issues=None,
                     pulls=None, workflows=None, watchers=None, page=None, sort=None):  # noqa: E501
    """Retrieve repositories with filtering options

    Retrieve repositories with filtering options # noqa: E501

    :param name: Filter repositories by name.  If providing a full name, prefix it with repo: (e.g., repo:owner/name). 
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
    :param watchers: Filter repositories by watchers range (e.g., 1,20)
    :type watchers: str
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int
    :param sort: Sort repositories by field in ascending or descending order  (e.g., field-asc or field-desc). If order is not specified, default to ascending. 
    :type sort: str

    :rtype: RepositoriesList
    """

    mongo_ops = MongoOperations()
    try:
        repositories_data = mongo_ops.get_repositories(name=name, language=language, is_private=is_private,
                                                       date_range=date_range, stars=stars, forks=forks, issues=issues,
                                                       pulls=pulls, workflows=workflows, watchers=watchers, page=page,
                                                       sort=sort)

        total = mongo_ops.count_repositories(name=name, language=language, is_private=is_private,
                                             date_range=date_range, stars=stars, forks=forks, issues=issues,
                                             pulls=pulls, workflows=workflows, watchers=watchers)

        repositories = [
            mapper.map_response_to_repository(repo)
            for repo in repositories_data
        ]

        response = RepositoriesList(items=repositories, total_elements=total, page=page).to_dict()
        return response, 200
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
    r = mapper.map_response_to_repository(repo).to_dict()
    return r, 200


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


def get_statistics(date_range, name=None, language=None, is_private=None, stars=None, forks=None, issues=None,
                   pulls=None, workflows=None, watchers=None):  # noqa: E501
    """Compute the statistics of all the filtered repositories

    Compute the statistics of all the filtered repositories.
    If you want not insert any filter the statistic will realize on every field.    # noqa: E501

    :param date_range: Filter repositories by date range (e.g., 2023-01-01,2023-12-31)
    :type date_range: str
    :param name: Filter repositories by name.
                 If providing a full name, prefix it with repo: (e.g., repo:owner/name).
    :type name: str
    :param language: Filter repositories by programming language
    :type language: str
    :param is_private: Filter private repositories
    :type is_private: bool
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
    :param watchers: Filter repositories by watchers range (e.g., 1,5)
    :type watchers: str

    :rtype: Statistics
    """
    error_message = validate_date_range(date_range)
    if error_message:
        return jsonify({"error": error_message}), 400

    repositories_response, status_code = get_repositories(name, language, is_private, date_range, stars, forks, issues,
                                                          pulls, workflows, watchers, -1)

    return __compute_stats(repositories_response["items"], date_range), 200


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
    error_message = validate_date_range(date_range)
    if error_message:
        return jsonify({"error": error_message}), 400

    repo = get_repository_by_full_name(owner, name)[0]

    return __compute_stats([repo], date_range), 200


def __compute_stats(repos, date_range):
    # Initialize a Statistics object
    stats = Statistics(StatisticsPulls(), StatisticsIssues(), StatisticsWorkflows(), StatisticsRepositories())

    # Iterate over each repository
    for repo in repos:
        # Get statistics for the current repository
        #owner, r_name = repo['full_name'].split('/')
        stats_issues, stats_pulls, stats_workflows, stats_repositories = __get_stats(repo['full_name'], date_range)

        # Accumulate statistics into the main stats object using the standalone function
        accumulate_stats(stats, stats_issues, stats_pulls, stats_workflows, stats_repositories)

    return stats.to_dict()


def __get_stats(full_name, date_range):
    """
    Retrieves and computes statistics related to issues, pull requests, workflows, and repositories
    for a given repository.

    :param full_name: The owner and name of the repository.
    :type full_name: str
    :param date_range: Date range filter for issues and pull requests (e.g., "2023-01-01,2023-12-31").
    :type date_range: str
    :return: Tuple containing statistics for issues, pull requests, workflows, and repositories.
    :rtype: Tuple[StatisticsIssues, StatisticsPulls, StatisticsWorkflows, StatisticsRepositories]
    """
    issues_data = {
        "OPEN": business.elaborate_issues(full_name, "issues", "OPEN", date_range, -1).items,
        "CLOSED": business.elaborate_issues(full_name, "issues", "CLOSED", date_range, -1).items,
    }

    pulls_data = {
        "OPEN": business.elaborate_issues(full_name, "pulls", "OPEN", date_range, -1).items,
        "CLOSED": business.elaborate_issues(full_name, "pulls", "CLOSED", date_range, -1).items,
        "MERGED": business.elaborate_issues(full_name, "pulls", "MERGED", date_range, -1).items
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
    combined_issues = issues_data["OPEN"] + issues_data["CLOSED"] + pulls_data["OPEN"] + pulls_data["CLOSED"]

    # Compute statistics for repositories
    stats_repositories = StatisticsRepositories(
        stats=generate_label_count_map(combined_issues)
    )

    # Compute statistics for workflows
    owner, name = full_name.split("/")
    workflows_data = get_workflows_of_repo(owner, name)[0]
    stats_workflows = StatisticsWorkflows(
        metrics=generate_metrics_workflow_map(workflows_data)
    )

    return stats_issues, stats_pulls, stats_workflows, stats_repositories
