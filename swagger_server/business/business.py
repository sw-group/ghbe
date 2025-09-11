from typing import List

from werkzeug.exceptions import NotFound, BadRequest

from swagger_server.db.mongo_operations import MongoOperations
from swagger_server.models import IssuesList, CommentsList, RepositoriesList, Metrics, Repository, Statistics, \
    StatisticsPulls, StatisticsIssues, StatisticsWorkflows, StatisticsRepositories
from swagger_server.utils import util, validation, mapper

mongo_ops = MongoOperations()


def elaborate_issues(full_name, state,
                     date_range, page, sort=None):
    """
    Retrieves a list of issues from a mongoDB collection based on specified criteria.

    :param full_name: Full name of the repository.
    :type full_name: str
    :param state: State of the issues ("OPEN" or "CLOSED").
    :type state: str
    :param date_range: Date range filter for issues (e.g., "2023-01-01,2023-12-31").
    :type date_range: str
    :param page: Page number for pagination.
    :type page: int
    :param sort: Sorting criteria.
    :type sort: str, optional
    :return: List of issues with pagination information.
    :rtype: IssuesList
    """
    issues_data = mongo_ops.get_issues(repo=full_name, state=state, date_range=date_range, page=page,
                                       sort=sort)

    total = mongo_ops.count_issues(repo=full_name, state=state, date_range=date_range)

    issues = [
        mapper.map_response_to_issue(i)
        for i in issues_data
    ]

    return IssuesList(items=issues, page=page, total_elements=total)

def elaborate_prs(full_name, state,
                  date_range, page, sort=None):
    """
    Retrieves a list of pull requests from a mongoDB collection based on specified criteria.

    :param full_name: Full name of the repository.
    :type full_name: str
    :param state: State of the pulls ("OPEN", "CLOSED", or "MERGED").
    :type state: str
    :param date_range: Date range filter for pull requests (e.g., "2023-01-01,2023-12-31").
    :type date_range: str
    :param page: Page number for pagination.
    :type page: int
    :param sort: Sorting criteria.
    :type sort: str, optional
    :return: List of pull requests with pagination information.
    :rtype: IssuesList
    """
    prs_data = mongo_ops.get_prs(repo=full_name, state=state, date_range=date_range, page=page,
                                       sort=sort)

    total = mongo_ops.count_prs(repo=full_name, state=state, date_range=date_range)

    prs = [
        mapper.map_response_to_issue(i)
        for i in prs_data
    ]

    return IssuesList(items=prs, page=page, total_elements=total)


def elaborate_issue_comments(full_name, issue_number, page):
    """
    Retrieves comments associated with a specific issue from a mongoDB collection.

    :param full_name: Full name of the repository.
    :type full_name: str
    :param issue_number: Issue number.
    :type issue_number: int
    :param page: Page number for pagination.
    :type page: int
    :return: List of comments for the specified issue with pagination information.
    :rtype: CommentsList
    """
    comments_data = mongo_ops.get_comments(repo=full_name, number=issue_number, page=page)

    total = mongo_ops.count_issue_comments(repo=full_name, number=issue_number)

    comments = [
        mapper.map_response_to_comment(c)
        for c in comments_data
    ]

    return CommentsList(items=comments, page=page, total_elements=total)


def elaborate_repositories(name=None, language=None, is_private=None, date_range=None,
                           stars=None, forks=None, issues=None, pulls=None,
                           workflows=None, watchers=None, page=None, sort=None) -> RepositoriesList:
    """
    Retrieves a list of repositories from a mongoDB collection based on specified criteria.

    :param name: Repository name filter.
    :type name: str, optional
    :param language: Programming language filter.
    :type language: str, optional
    :param is_private: Private repository filter.
    :type is_private: bool, optional
    :param date_range: Date range filter for repository creation.
    :type date_range: str, optional
    :param stars: Filter minimum and maximum stars filter.
    :type stars: str, optional
    :param forks: Filter minimum and maximum forks filter.
    :type forks: str, optional
    :param issues: Filter minimum and maximum issues filter.
    :type issues: str, optional
    :param pulls: Filter minimum and maximum pull requests filter.
    :type pulls: str, optional
    :param workflows: Filter minimum and maximum workflows filter.
    :type workflows: str, optional
    :param watchers: Filter minimum and maximum watchers filter.
    :type watchers: str, optional
    :param page: Page number for pagination.
    :type page: int, optional
    :param sort: Sorting criteria.
    :type sort: str, optional
    :return: List of repositories matching the specified criteria with pagination information.
    :rtype: RepositoriesList
    """

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

    return RepositoriesList(items=repositories, total_elements=total, page=page)


def elaborate_repository(full_name):
    """
    Retrieves information about a specific repository from a mongoDB collection.

    :param full_name: Full name of the repository.
    :type full_name: str
    :return: Repository information.
    :rtype: Repository
    :raises NotFound: If the repository does not exist.
    """
    repositories_data = mongo_ops.get_repository(full_name)

    if repositories_data is None:
        raise NotFound

    return mapper.map_response_to_repository(repositories_data)


def elaborate_workflows(full_name):
    """
    Retrieves workflows associated with a specific repository from a mongoDB collection.

    :param full_name: Full name of the repository.
    :type full_name: str
    :return: List of workflows for the specified repository.
    :rtype: List[Workflow]
    :raises NotFound: If the repository does not exist.
    """
    if not mongo_ops.get_repository(full_name):
        raise NotFound

    workflows_data = mongo_ops.get_workflows(full_name)

    workflows = [
        mapper.map_response_to_workflow(w)
        for w in workflows_data.get('workflows', [])
    ]

    return workflows


def elaborate_statistics(date_range_stats, name, language, is_private, date_range, stars,
                         forks, issues, pulls, workflows, watchers):
    """
    Retrieves and computes statistics for repositories based on specified criteria.

    :param date_range_stats: Date range filter for stats creation.
    :type date_range_stats: str
    :param name: Repository name filter.
    :type name: str
    :param language: Programming language filter.
    :type language: str
    :param is_private: Private repository filter.
    :type is_private: bool
    :param date_range: Date range filter for repository creation.
    :type date_range: str
    :param stars: Filter minimum and maximum stars filter.
    :type stars: str
    :param forks: Filter minimum and maximum forks filter.
    :type forks: str
    :param issues: Filter minimum and maximum issues filter.
    :type issues: str
    :param pulls: Filter minimum and maximum pull requests filter.
    :type pulls: str
    :param workflows: Filter minimum and maximum workflows filter.
    :type workflows: str
    :param watchers: Filter minimum and maximum watchers filter.
    :type watchers: str
    :return: Statistics computed for the matching repositories.
    :rtype: Statistics
    """
    error_message = validation.validate_date_range(date_range_stats)
    if error_message:
        raise BadRequest(error_message)

    repositories_response = elaborate_repositories(name, language, is_private, date_range, stars,
                                                   forks, issues, pulls, workflows, watchers, -1)

    return __compute_stats(repositories_response.items, date_range_stats)


def elaborate_statistic(full_name, date_range):
    """
    Retrieves and computes statistics for a specific repository based on specified criteria.

    :param full_name: Full name of the repository.
    :type full_name: str
    :param date_range: Date range filter for issues and pull requests (e.g., "2023-01-01,2023-12-31").
    :type date_range: str
    :return: Statistics computed for the repository.
    :rtype: Statistics
    """
    error_message = validation.validate_date_range(date_range)
    if error_message:
        raise BadRequest(error_message)

    repositories_response = elaborate_repository(full_name)

    return __compute_stats([repositories_response], date_range)


def elaborate_metrics_repositories():
    """
    Retrieves and computes metrics (e.g., maximum counts for stars, watchers, forks, etc.)
    for all repositories.

    :return: Metrics computed across all repositories.
    :rtype: Metrics
    """
    repositories = elaborate_repositories(page=-1).items

    languages = set()
    maxes = {
        'stars_count': 0,
        'watchers_count': 0,
        'forks_count': 0,
        'issue_count': 0,
        'pr_count': 0,
        'workflows_count': 0
    }

    for repo in repositories:
        repo_dict = repo.to_dict()
        languages.add(repo.language)

        for key in maxes.keys():
            maxes[key] = max(maxes[key], repo_dict[key])

    return Metrics(
        languages=list(languages),
        maxes=maxes
    )


def __compute_stats(repos: List[Repository], date_range):
    """
    Computes overall statistics (issues, pull requests, workflows, repositories) from a list of repositories.

    :param repos: List of repositories.
    :type repos: List[Repository]
    :param date_range: Date range filter for issues and pull requests (e.g., "2023-01-01,2023-12-31").
    :type date_range: str
    :return: Overall statistics computed for the repositories.
    :rtype: Statistics
    """
    # Initialize a Statistics object
    stats = Statistics(StatisticsPulls(), StatisticsIssues(), StatisticsWorkflows(), StatisticsRepositories())

    # Iterate over each repository
    for repo in repos:
        # Get statistics for the current repository
        stats_issues, stats_pulls, stats_workflows, stats_repositories = __get_stats(repo.full_name, date_range)

        # Accumulate statistics into the main stats object using the standalone function
        util.accumulate_stats(stats, stats_issues, stats_pulls, stats_workflows, stats_repositories)

    return stats


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
        "OPEN": elaborate_issues(full_name, "OPEN", date_range, -1).items,
        "CLOSED": elaborate_issues(full_name, "CLOSED", date_range, -1).items,
    }

    pulls_data = {
        "OPEN": elaborate_prs(full_name, "OPEN", date_range, -1).items,
        "CLOSED": elaborate_prs(full_name, "CLOSED", date_range, -1).items,
        "MERGED": elaborate_prs(full_name, "MERGED", date_range, -1).items
    }

    # Compute statistics for issues
    stats_issues = StatisticsIssues(
        daily_closed_progress=util.generate_date_count_map(issues_data["CLOSED"]),
        daily_opened_progress=util.generate_date_count_map(issues_data["OPEN"])
    )

    # Compute statistics for pulls
    stats_pulls = StatisticsPulls(
        daily_closed_progress=util.generate_date_count_map(pulls_data["CLOSED"]),
        daily_opened_progress=util.generate_date_count_map(pulls_data["OPEN"]),
        merged=len(pulls_data["MERGED"])
    )

    # Combine issues and pulls data for repository statistics
    combined_issues = issues_data["OPEN"] + issues_data["CLOSED"] + pulls_data["OPEN"] + pulls_data["CLOSED"]

    # Compute statistics for repositories
    stats_repositories = StatisticsRepositories(
        stats=util.generate_label_count_map(combined_issues)
    )

    # Compute statistics for workflows
    workflows_data = elaborate_workflows(full_name)
    stats_workflows = StatisticsWorkflows(
        metrics=util.generate_metrics_workflow_map(workflows_data)
    )

    return stats_issues, stats_pulls, stats_workflows, stats_repositories
