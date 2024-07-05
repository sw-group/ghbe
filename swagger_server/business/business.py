from swagger_server.db.mongo_operations import MongoOperations
from swagger_server.models import IssuesList, Metrics
from swagger_server.utils import mapper


def elaborate_issues(full_name: str, type_issue: str, state: str, date_range: str, page: int, sort: str = None):
    mongo_ops = MongoOperations(collection_name=("issues" if type_issue == "issues" else "pullRequests"))

    try:
        issues_data = mongo_ops.get_issues(repo=full_name, state=state, date_range=date_range, page=page,
                                           sort=sort)

        total = mongo_ops.count_issues(repo=full_name, state=state, date_range=date_range)

        issues = [
            mapper.map_response_to_issue(issue)
            for issue in issues_data
        ]

        return IssuesList(items=issues, page=page, total_elements=total)

    finally:
        mongo_ops.close()


# Function to extract required information
def elaborate_metrics_repositories(repos):
    languages = set()
    maxes = {
        'stars_count': 0,
        'watchers_count': 0,
        'forks_count': 0,
        'issue_count': 0,
        'pull_request_count': 0,
        'workflows_count': 0
    }

    for repo in repos:
        data = repo['data']
        languages.add(data['language'])

        for key in maxes.keys():
            if data[key] > maxes[key]:
                maxes[key] = data[key]

    result = Metrics(
        languages=list(languages),
        maxes=maxes
    )

    return result
