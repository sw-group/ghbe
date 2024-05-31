from swagger_server import util
from swagger_server.models import Repository, Workflow


def map_response_to_repository(response):
    response = response.get('response', {})

    return Repository(
        full_name=response.get('full_name'),
        url=response.get('url'),
        private=response.get('private', False),
        language=response.get('language'),
        created_at=util.deserialize_datetime(response['created_at']) if 'created_at' in response else None,
        updated_at=util.deserialize_datetime(response['updated_at']) if 'updated_at' in response else None,
        pushed_at=util.deserialize_datetime(response['pushed_at']) if 'pushed_at' in response else None,
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
        created_at=util.deserialize_datetime(response['created_at']) if 'created_at' in response else None,
        updated_at=util.deserialize_datetime(response['updated_at']) if 'updated_at' in response else None,
        file_url=response.get('html_url')  # Assuming 'html_url' contains the file URL
    )

