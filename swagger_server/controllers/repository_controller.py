from swagger_server.business import business
from swagger_server.models.comments_list import CommentsList  # noqa: E501
from swagger_server.models.issues_list import IssuesList  # noqa: E501
from swagger_server.models.repositories_list import RepositoriesList  # noqa: E501
from swagger_server.models.repository import Repository  # noqa: E501
from swagger_server.models.statistics import Statistics  # noqa: E501
from flask import jsonify, request


def get_comments_of_issue(owner, name, number, page=None):  # noqa: E501
    """Search issues of the repo by fullname

    Search issues of the repo by fullname # noqa: E501

    :param owner: The owner of the repository
    :type owner: str
    :param name: The name of the repository
    :type name: str
    :param number: The number of the issue
    :type number: int
    :param page: Specify the page number for paginated results (default is 1)
    :type page: int

    :rtype: CommentsList
    """
    repo_full_name = f'{owner}/{name}'
    return business.elaborate_issue_comments(repo_full_name, number, page).to_dict()


def get_issues_of_repo(owner, name, issue_type, state=None, date_range=None, page=None, sort=None):  # noqa: E501
    """
    Search issues of the repo by fullname

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
    return business.elaborate_repositories(name, language, is_private, date_range, stars, forks, issues, pulls,
                                           workflows, watchers, page, sort).to_dict()


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
    return business.elaborate_repository(repo_full_name).to_dict()


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
    workflows = business.elaborate_workflows(repo_full_name)
    return [workflow.to_dict() for workflow in workflows]


def get_statistics(date_range_stats, name=None, language=None, is_private=None, date_range=None, stars=None, forks=None, issues=None,
                   pulls=None, workflows=None, watchers=None):  # noqa: E501
    """Compute the statistics of all the filtered repositories

    Compute the statistics of all the filtered repositories.
    If you want not insert any filter the statistic will realize on every field.    # noqa: E501

    :param date_range_stats: Filter stats by date range (e.g., 2023-01-01,2023-12-31), relative to updated date of issues/pr
    :type date_range_stats: str
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
    :param watchers: Filter repositories by watchers range (e.g., 1,5)
    :type watchers: str
    :param date_range_stats: Filter stats by date range (e.g., 2023-01-01,2023-12-31), relative to updated date of issues/pr
    :type date_range_stats: str

    :rtype: Statistics
    """
    return business.elaborate_statistics(date_range_stats, name, language, is_private, date_range, stars, forks, issues,
                                         pulls, workflows, watchers).to_dict()


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
    repo_full_name = f"{owner}/{name}"
    return business.elaborate_statistic(repo_full_name, date_range).to_dict()


def register_repository_routes(app):
    # /repositories
    @app.route("/repositories", methods=["GET"])
    def repositories_route():
        return jsonify(get_repositories(
            name=request.args.get("name"),
            language=request.args.get("language"),
            is_private=request.args.get("isPrivate") == "true",
            date_range=request.args.get("dateRange"),
            stars=request.args.get("stars"),
            forks=request.args.get("forks"),
            issues=request.args.get("issues"),
            pulls=request.args.get("pulls"),
            workflows=request.args.get("workflows"),
            watchers=request.args.get("watchers"),
            page=int(request.args.get("page", 1)) if request.args.get("page") else 1,
            sort=request.args.get("sort")
        ))

    # /repositories/statistics
    @app.route("/repositories/statistics", methods=["GET"])
    def repositories_statistics_route():
        return jsonify(get_statistics(
            date_range_stats=request.args.get("dateRangeStats"),
            name=request.args.get("name"),
            language=request.args.get("language"),
            is_private=request.args.get("isPrivate") == "true",
            date_range=request.args.get("dateRange"),
            stars=request.args.get("stars"),
            forks=request.args.get("forks"),
            issues=request.args.get("issues"),
            pulls=request.args.get("pulls"),
            workflows=request.args.get("workflows"),
            watchers=request.args.get("watchers")
        ))

    # /repositories/{owner}/{name}
    @app.route("/repositories/<owner>/<name>", methods=["GET"])
    def repository_by_full_name_route(owner, name):
        return jsonify(get_repository_by_full_name(owner, name))

    # /repositories/{owner}/{name}/workflows
    @app.route("/repositories/<owner>/<name>/workflows", methods=["GET"])
    def workflows_of_repo_route(owner, name):
        return jsonify(get_workflows_of_repo(owner, name))

    # /repositories/{owner}/{name}/issues
    @app.route("/repositories/<owner>/<name>/issues", methods=["GET"])
    def issues_of_repo_route(owner, name):
        return jsonify(get_issues_of_repo(
            owner,
            name,
            issue_type=request.args.get("issue_type"),
            state=request.args.get("state"),
            date_range=request.args.get("dateRange"),
            page=int(request.args.get("page", 1)) if request.args.get("page") else 1,
            sort=request.args.get("sort")
        ))

    # /repositories/{owner}/{name}/issues/{number}/comments
    @app.route("/repositories/<owner>/<name>/issues/<int:number>/comments", methods=["GET"])
    def comments_of_issue_route(owner, name, number):
        return jsonify(get_comments_of_issue(
            owner,
            name,
            number,
            page=int(request.args.get("page", 1)) if request.args.get("page") else 1,
        ))

    # /repositories/{owner}/{name}/statistics
    @app.route("/repositories/<owner>/<name>/statistics", methods=["GET"])
    def statistics_of_repository_route(owner, name):
        return jsonify(get_statistics_of_repository(
            owner,
            name,
            date_range=request.args.get("dateRange")
        ))

