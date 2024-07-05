import pytest
import unittest
from unittest.mock import patch, MagicMock
from werkzeug.exceptions import NotFound
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
    def test_elaborate_issues(self, MockMongoOperations):
        mock_mongo_ops = MockMongoOperations.return_value
        mock_mongo_ops.get_issues.return_value = []
        mock_mongo_ops.count_issues.return_value = 0

        result = elaborate_issues("repo/test", "issues", "OPEN", "2023-01-01,2023-12-31", 1)
        self.assertIsInstance(result, IssuesList)
        self.assertEqual(result.items, [])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 0)

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_issue_comments(self, MockMongoOperations):
        mock_mongo_ops = MockMongoOperations.return_value
        mock_mongo_ops.get_comments.return_value = []
        mock_mongo_ops.count_issue_comments.return_value = 0

        result = elaborate_issue_comments("repo/test", 1, 1)
        self.assertIsInstance(result, CommentsList)
        self.assertEqual(result.items, [])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 0)

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_repositories(self, MockMongoOperations):
        mock_mongo_ops = MockMongoOperations.return_value
        mock_mongo_ops.get_repositories.return_value = []
        mock_mongo_ops.count_repositories.return_value = 0

        result = elaborate_repositories(page=1)
        self.assertIsInstance(result, RepositoriesList)
        self.assertEqual(result.items, [])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 0)

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_repository(self, MockMongoOperations):
        mock_mongo_ops = MockMongoOperations.return_value
        mock_mongo_ops.get_repository.return_value = None

        with self.assertRaises(NotFound):
            elaborate_repository("repo/test")

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_workflows(self, MockMongoOperations):
        mock_mongo_ops = MockMongoOperations.return_value
        mock_mongo_ops.get_repository.return_value = True
        mock_mongo_ops.get_workflows.return_value = {'workflows': []}

        result = elaborate_workflows("repo/test")
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    @patch('swagger_server.business.business.elaborate_repositories')
    def test_elaborate_statistics(self, mock_elaborate_repositories):
        mock_elaborate_repositories.return_value = RepositoriesList(items=[], total_elements=0, page=-1)

        with patch('swagger_server.utils.validation.validate_date_range', return_value=None):
            result = elaborate_statistics("2023-01-01,2023-12-31", None, None, None, None, None, None, None, None, None)
            self.assertIsInstance(result, Statistics)

    @patch('swagger_server.business.business.elaborate_repository')
    def test_elaborate_statistic(self, mock_elaborate_repository):
        #TODO: Test the doesn't exist repository!
        mock_elaborate_repository.return_value = Repository(full_name="helium/miner")

        with patch('swagger_server.utils.validation.validate_date_range', return_value=None):
            result = elaborate_statistic("helium/miner", "2023-01-01,2023-12-31")
            self.assertIsInstance(result, Statistics)

    @patch('swagger_server.business.business.elaborate_repositories')
    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_metrics_repositories(self, MockMongoOperations, mock_elaborate_repositories):
        mock_elaborate_repositories.return_value = RepositoriesList(items=[], total_elements=0, page=-1)

        result = elaborate_metrics_repositories()
        self.assertIsInstance(result, Metrics)


if __name__ == '__main__':
    import unittest
    unittest.main()
