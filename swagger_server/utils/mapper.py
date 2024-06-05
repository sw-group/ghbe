from swagger_server import util
from swagger_server.models import Repository, Workflow, Issue, IssueLabels, IssueComments, Comment


def map_response_to_repository(response):
    response = response.get('data', {})

    return Repository(
        full_name=response.get('full_name'),
        url=response.get('url'),
        private=response.get('private', False),
        language=response.get('language'),
        created_at=util.deserialize_datetime(response['created_at']) if response.get('created_at') else None,
        updated_at=util.deserialize_datetime(response['updated_at']) if response.get('updated_at') else None,
        pushed_at=util.deserialize_datetime(response['pushed_at']) if response.get('pushed_at') else None,
        stars_count=response.get('stars_count'),
        forks_count=response.get('forks_count'),
        watchers_count=response.get('watchers_count'),
        issue_count=response.get('issue_count'),
        pr_count=response.get('pull_request_count'),  # Adjusting the key name
        workflows_count=response.get('workflows_count')
    )


def map_response_to_workflow(response):
    return Workflow(
        id=response.get('id'),
        name=response.get('name'),
        path=response.get('path'),
        url=response.get('url'),
        state=response.get('state'),
        created_at=util.deserialize_datetime(response['created_at']) if response.get('created_at') else None,
        updated_at=util.deserialize_datetime(response['updated_at']) if response.get('updated_at') else None,
        file_url=response.get('html_url')  # Assuming 'html_url' contains the file URL
    )


def map_response_to_issue(repo, issue):
    """Maps a dictionary from MongoDB to an Issue instance."""
    return Issue(
        number=issue.get('number'),
        repo=repo,
        title=issue.get('title'),
        url=issue.get('url'),
        state=issue.get('state'),
        body=issue.get('body'),
        author=issue.get('author'),
        labels=map_issue_labels(dict(issue.get('labels', []))),
        comments=map_issue_comments(dict(issue.get('comments', {}))) if issue.get('comments') else None,
        created_at=util.deserialize_datetime(issue.get('createdAt')) if issue.get('createdAt') else None,
        updated_at=util.deserialize_datetime(issue.get('updatedAt')) if issue.get('updatedAt') else None,
        closed_at=util.deserialize_datetime(issue.get('closedAt')) if issue.get('closedAt') else None,
    )


def map_issue_labels(label_dicts):
    """Maps a list of dictionaries to a list of IssueLabels instances."""
    return [IssueLabels.from_dict(label) for label in label_dicts.get('nodes')]


def map_issue_comments(comment_dict):
    """Maps a dictionary to an IssueComments instance."""
    return IssueComments(
        total=comment_dict.get('totalCount'),
        list=[map_comment_info(dict(comment)) for comment in comment_dict.get('nodes')]
    )


def map_comment_info(comment):
    return Comment(
        author=comment.get('author'),
        message=comment.get('body'),
        created_at=util.deserialize_datetime(comment.get('createdAt')) if comment.get('createdAt') else None,
        updated_at=util.deserialize_datetime(comment['updatedAt']) if comment.get('updatedAt') else None
    )
