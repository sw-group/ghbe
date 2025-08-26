import pytest
import unittest
from unittest.mock import patch, MagicMock
from werkzeug.exceptions import NotFound, BadRequest
import swagger_server.business.business as business

from swagger_server.business.business import (
    elaborate_issues,
    elaborate_issue_comments,
    elaborate_repositories,
    elaborate_repository,
    elaborate_workflows,
    elaborate_statistics,
    elaborate_statistic,
    elaborate_metrics_repositories
)
from swagger_server.models import (
    IssuesList, CommentsList, RepositoriesList,
    Repository, Workflow, Metrics, Statistics
)

class TestElaborateFunctions(unittest.TestCase):

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_issue')
    def test_elaborate_issues_success(self, mock_mapper, MockMongoOperations):
        """Test elaborate_issues normal path"""
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_issues.return_value = [{"id": 1}]
        mock_mongo.count_issues.return_value = 1
        mock_mapper.return_value = {"mapped": "issue"}

        result = elaborate_issues("repo/test", "issues", "OPEN", "2023-01-01,2023-12-31", 1)
        self.assertIsInstance(result, IssuesList)
        self.assertEqual(result.total_elements, 1)
        self.assertEqual(result.items, [{"mapped": "issue"}])
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_comment')
    def test_elaborate_issue_comments_success(self, mock_mapper, MockMongoOperations):
        """Test elaborate_issue_comments normal path"""
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_comments.return_value = [{"id": 1}]
        mock_mongo.count_issue_comments.return_value = 1
        mock_mapper.return_value = {"mapped": "comment"}

        result = elaborate_issue_comments("repo/test", 1, 1)
        self.assertIsInstance(result, CommentsList)
        self.assertEqual(result.items, [{"mapped": "comment"}])
        self.assertEqual(result.total_elements, 1)
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_repository')
    def test_elaborate_repositories_success(self, mock_mapper, MockMongoOperations):
        """Test elaborate_repositories normal path"""
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_repositories.return_value = [{"name": "repo"}]
        mock_mongo.count_repositories.return_value = 1
        mock_mapper.return_value = {"mapped": "repo"}

        result = elaborate_repositories(page=1)
        self.assertIsInstance(result, RepositoriesList)
        self.assertEqual(result.items, [{"mapped": "repo"}])
        self.assertEqual(result.total_elements, 1)
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_repository_not_found(self, mock_mongo_ops):
        """Trigger line 150: repositories_data is None → NotFound"""
        mock_instance = mock_mongo_ops.return_value
        mock_instance.get_repository.return_value = None

        with self.assertRaises(NotFound):
            elaborate_repository("owner/nonexistent-repo")

        mock_instance.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_workflow')
    def test_elaborate_workflows_success(self, mock_mapper, MockMongoOperations):
        """Test elaborate_workflows normal path"""
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_repository.return_value = True
        mock_mongo.get_workflows.return_value = {"workflows": [{"name": "wf"}]}
        mock_mapper.return_value = {"mapped": "workflow"}

        result = elaborate_workflows("repo/test")
        self.assertIsInstance(result, list)
        self.assertEqual(result, [{"mapped": "workflow"}])
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_workflows_not_found(self, mock_mongo_ops):
        """Trigger line 168: repo not found → NotFound"""
        mock_instance = mock_mongo_ops.return_value
        mock_instance.get_repository.return_value = False  # Simulate repo not found

        with self.assertRaises(NotFound):
            elaborate_workflows("owner/nonexistent-repo")

        mock_instance.close.assert_called_once()

    @patch('swagger_server.business.business.elaborate_repositories')
    @patch('swagger_server.business.business.validation.validate_date_range', return_value=None)
    def test_elaborate_statistics_success(self, mock_validate, mock_repos):
        """Test elaborate_statistics normal path"""
        mock_repos.return_value.items = []
        result = elaborate_statistics("2023-01-01,2023-12-31", None, None, None, None, None, None, None, None, None)
        self.assertIsInstance(result, Statistics)

    @patch('swagger_server.business.business.validation.validate_date_range', return_value="Invalid date range")
    def test_elaborate_statistics_invalid_date(self, mock_validate):
        """Trigger line 212: invalid date range → BadRequest"""
        with self.assertRaises(BadRequest):
            elaborate_statistics("invalid-date-range", None, None, None, None, None, None, None, None, None)

        mock_validate.assert_called_once_with("invalid-date-range")

    @patch('swagger_server.business.business.elaborate_workflows', return_value=[])
    @patch('swagger_server.business.business.elaborate_repository')
    @patch('swagger_server.business.business.validation.validate_date_range', return_value=None)
    def test_elaborate_statistic_success(self, mock_validate, mock_elaborate_repo, mock_elaborate_workflows):
        # Simulate a repo existing
        mock_repo = Repository(full_name="repo/owner")
        mock_repo.to_dict = MagicMock(return_value={
            'stars_count': 10,
            'watchers_count': 5,
            'forks_count': 2,
            'issue_count': 1,
            'pr_count': 0,
            'workflows_count': 0,
            'language': 'Python'
        })
        mock_elaborate_repo.return_value = mock_repo

        # Act
        result = elaborate_statistic("repo/owner", "2023-01-01,2023-12-31")

        # Assert
        self.assertIsInstance(result, Statistics)
        mock_elaborate_repo.assert_called_once_with("repo/owner")
        mock_validate.assert_called_once_with("2023-01-01,2023-12-31")
        mock_elaborate_workflows.assert_called_once_with("repo/owner")

    @patch('swagger_server.business.business.validation.validate_date_range', return_value="Invalid range")
    def test_elaborate_statistic_invalid_date(self, mock_validate):
        """Test invalid date range raises BadRequest"""
        with self.assertRaises(BadRequest):
            elaborate_statistic("helium/miner", "invalid-date")

        mock_validate.assert_called_once_with("invalid-date")

    @patch('swagger_server.business.business.elaborate_repositories')
    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_metrics_repositories_success(self, MockMongoOperations, mock_repos):
        """Test elaborate_metrics_repositories normal path"""
        mock_repos.return_value.items = []
        result = elaborate_metrics_repositories()
        self.assertIsInstance(result, Metrics)

    @patch('swagger_server.business.business.mapper.map_response_to_repository')
    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_repository_mapper_call(self, mock_mongo_ops, mock_mapper):
        """Cover row 150: execute mapper.map_response_to_repository"""
        mock_instance = mock_mongo_ops.return_value
        mock_instance.get_repository.return_value = {"full_name": "repo/owner"}  # simulate DB response

        mock_mapper.return_value = Repository(full_name="repo/owner")  # mapper returns Repository model

        result = business.elaborate_repository("repo/owner")

        self.assertIsInstance(result, Repository)
        mock_instance.get_repository.assert_called_once_with("repo/owner")
        mock_mapper.assert_called_once_with({"full_name": "repo/owner"})
        mock_instance.close.assert_called_once()


if __name__ == '__main__':
    import unittest
    unittest.main()
