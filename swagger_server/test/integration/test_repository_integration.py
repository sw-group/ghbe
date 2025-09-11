# coding: utf-8

from __future__ import absolute_import

from swagger_server.test import BaseTestCase

class TestRepositoryController(BaseTestCase):
    """RepositoryController integration test stubs"""

    def test_get_repositories(self):
        """Test GET /repositories"""
        response = self.client.get('/repositories', query_string={
            'name': 'repo:owner/name',
            'language': 'python',
            'isPrivate': 'false',
            'stars': '0,100',
            'page': 1
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)  # should match RepositoriesList dict structure

    def test_get_repository_by_full_name(self):
        """Test GET /repositories/{owner}/{name}"""
        response = self.client.get('/repositories/owner_example/name_example')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsInstance(data, dict)  # should match Repository dict structure

    def test_get_workflows_of_repo(self):
        """Test GET /repositories/{owner}/{name}/workflows"""
        response = self.client.get('/repositories/owner_example/name_example/workflows')
        self.assertEqual(response.status_code, 404)

    def test_get_issues_of_repo(self):
        """Test GET /repositories/{owner}/{name}/issues"""
        response = self.client.get('/repositories/owner_example/name_example/issues', query_string={
            'issue_type': 'issues',
            'state': 'open',
            'page': 1
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)  # should match IssuesList dict structure

    def test_get_comments_of_issue(self):
        """Test GET /repositories/{owner}/{name}/issues/{number}/comments"""
        response = self.client.get('/repositories/owner_example/name_example/issues/56/comments', query_string={
            'page': 1
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)  # should match CommentsList dict structure

    def test_get_statistics(self):
        """Test GET /repositories/statistics"""
        response = self.client.get('/repositories/statistics', query_string={
            'dateRangeStats': '2014-01-01,2014-01-31'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)  # should match Statistics dict structure

    def test_get_statistics_invalid_date_range(self):
        response = self.client.get('/repositories/statistics', query_string={
            'dateRangeStats': '2014-01-01,2014-12-31'
        })
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn('dateRange cannot exceed 1 month', str(data))

    def test_get_statistics_of_repository(self):
        """Test GET /repositories/{owner}/{name}/statistics"""
        response = self.client.get('/repositories/owner_example/name_example/statistics', query_string={
            'dateRange': '2014-01-01,2014-01-31'
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIsInstance(data, dict)  # should match Statistics dict structure


if __name__ == '__main__':
    import unittest
    unittest.main()
