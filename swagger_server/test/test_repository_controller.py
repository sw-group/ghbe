# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO
from swagger_server.test import BaseTestCase

from swagger_server.models.comments_list import CommentsList  # noqa: E501
from swagger_server.models.issues_list import IssuesList  # noqa: E501
from swagger_server.models.repositories_list import RepositoriesList  # noqa: E501
from swagger_server.models.repository import Repository  # noqa: E501
from swagger_server.models.statistics import Statistics  # noqa: E501
from swagger_server.models.workflow import Workflow  # noqa: E501


class TestRepositoryController(BaseTestCase):
    """RepositoryController integration test stubs"""

    def test_get_comments_of_issue(self):
        """Test case for get_comments_of_issue

        Search issues of the repo by fullname
        """
        query_string = [('page', 1)]
        response = self.client.open(
            '/ghbe/api/v1/repositories/{owner}/{name}/issues/{number}/comments'.format(owner='owner_example', name='name_example', number=56),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_issues_of_repo(self):
        """Test case for get_issues_of_repo

        Search issues of the repo by fullname
        """
        query_string = [('issue_type', 'issues'),
                        ('state', 'state_example'),
                        ('date_range', 'date_range_example'),
                        ('page', 1),
                        ('sort', 'sort_example')]
        response = self.client.open(
            '/ghbe/api/v1/repositories/{owner}/{name}/issues'.format(owner='owner_example', name='name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_repositories(self):
        """Test case for get_repositories

        Retrieve repositories with filtering options
        """
        query_string = [('name', 'name_example'),
                        ('language', 'language_example'),
                        ('is_private', True),
                        ('date_range', 'date_range_example'),
                        ('stars', 'stars_example'),
                        ('forks', 'forks_example'),
                        ('issues', 'issues_example'),
                        ('pulls', 'pulls_example'),
                        ('workflows', 'workflows_example'),
                        ('watchers', 'watchers_example'),
                        ('page', 1),
                        ('sort', 'sort_example')]
        response = self.client.open(
            '/ghbe/api/v1/repositories',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_repository_by_full_name(self):
        """Test case for get_repository_by_full_name

        Search repositories by filter
        """
        response = self.client.open(
            '/ghbe/api/v1/repositories/{owner}/{name}'.format(owner='owner_example', name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_statistics(self):
        """Test case for get_statistics

        Compute the statistics of all the filtered repositories
        """
        query_string = [('name', 'name_example'),
                        ('language', 'language_example'),
                        ('is_private', True),
                        ('date_range', 'date_range_example'),
                        ('stars', 'stars_example'),
                        ('forks', 'forks_example'),
                        ('issues', 'issues_example'),
                        ('pulls', 'pulls_example'),
                        ('workflows', 'workflows_example'),
                        ('watchers', 'watchers_example')]
        response = self.client.open(
            '/ghbe/api/v1/repositories/statistics',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_statistics_of_repository(self):
        """Test case for get_statistics_of_repository

        Compute the statistics of a repository
        """
        query_string = [('date_range', 'date_range_example')]
        response = self.client.open(
            '/ghbe/api/v1/repositories/{owner}/{name}/statistics'.format(owner='owner_example', name='name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_workflows_of_repo(self):
        """Test case for get_workflows_of_repo

        Search workflows of the repo by fullname
        """
        response = self.client.open(
            '/ghbe/api/v1/repositories/{owner}/{name}/workflows'.format(owner='owner_example', name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
