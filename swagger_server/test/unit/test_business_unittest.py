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
    Repository, Metrics, Statistics
)


# -------------------
# White Box Unit Tests
# -------------------
class TestBusinessLayerWhiteBox(unittest.TestCase):

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_issue')
    def test_elaborate_issues(self, mock_mapper, MockMongoOperations):
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_issues.return_value = [{"id": 1}]
        mock_mongo.count_issues.return_value = 1
        mock_mapper.return_value = {"mapped": "issue"}

        result = elaborate_issues("repo/test", "issues", "OPEN", "2023-01-01,2023-12-31", 1)
        self.assertIsInstance(result, IssuesList)
        self.assertEqual(result.items, [{"mapped": "issue"}])
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_comment')
    def test_elaborate_issue_comments(self, mock_mapper, MockMongoOperations):
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_comments.return_value = [{"id": 1}]
        mock_mongo.count_issue_comments.return_value = 1
        mock_mapper.return_value = {"mapped": "comment"}

        result = elaborate_issue_comments("repo/test", 1, 1)
        self.assertIsInstance(result, CommentsList)
        self.assertEqual(result.items, [{"mapped": "comment"}])
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_repository')
    def test_elaborate_repositories(self, mock_mapper, MockMongoOperations):
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_repositories.return_value = [{"name": "repo"}]
        mock_mongo.count_repositories.return_value = 1
        mock_mapper.return_value = {"mapped": "repo"}

        result = elaborate_repositories(page=1)
        self.assertIsInstance(result, RepositoriesList)
        self.assertEqual(result.items, [{"mapped": "repo"}])
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_repository')
    def test_elaborate_repository_mapper_call(self, mock_mapper, MockMongoOperations):
        # Cover line 150
        mock_instance = MockMongoOperations.return_value
        mock_instance.get_repository.return_value = {"full_name": "repo/owner"}
        mock_mapper.return_value = Repository(full_name="repo/owner")

        result = elaborate_repository("repo/owner")
        self.assertIsInstance(result, Repository)
        mock_mapper.assert_called_once_with({"full_name": "repo/owner"})
        mock_instance.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_repository_not_found(self, MockMongoOperations):
        # Trigger NotFound
        mock_instance = MockMongoOperations.return_value
        mock_instance.get_repository.return_value = None

        with self.assertRaises(NotFound):
            elaborate_repository("owner/nonexistent-repo")
        mock_instance.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    @patch('swagger_server.business.business.mapper.map_response_to_workflow')
    def test_elaborate_workflows_success(self, mock_mapper, MockMongoOperations):
        mock_mongo = MockMongoOperations.return_value
        mock_mongo.get_repository.return_value = True
        mock_mongo.get_workflows.return_value = {"workflows": [{"name": "wf"}]}
        mock_mapper.return_value = {"mapped": "workflow"}

        result = elaborate_workflows("repo/test")
        self.assertIsInstance(result, list)
        self.assertEqual(result, [{"mapped": "workflow"}])
        mock_mongo.close.assert_called_once()

    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_workflows_not_found(self, MockMongoOperations):
        # Cover line 168
        mock_instance = MockMongoOperations.return_value
        mock_instance.get_repository.return_value = False

        with self.assertRaises(NotFound):
            elaborate_workflows("owner/nonexistent-repo")
        mock_instance.close.assert_called_once()


# -------------------
# Black Box Unit Tests
# -------------------
class TestBusinessLayerBlackBox(unittest.TestCase):

    @patch('swagger_server.business.business.elaborate_repositories')
    @patch('swagger_server.business.business.validation.validate_date_range', return_value=None)
    def test_elaborate_statistics_success(self, mock_validate, mock_repos):
        mock_repos.return_value.items = []
        result = elaborate_statistics("2023-01-01,2023-12-31", None, None, None, None, None, None, None, None, None)
        self.assertIsInstance(result, Statistics)

    @patch('swagger_server.business.business.elaborate_repositories')
    @patch('swagger_server.business.business.validation.validate_date_range', return_value="Invalid date range")
    def test_elaborate_statistics_invalid_date(self, mock_validate, mock_repos):
        # Cover line 212
        mock_repos.return_value.items = []
        with self.assertRaises(BadRequest):
            elaborate_statistics("invalid-date-range", None, None, None, None, None, None, None, None, None)
        mock_validate.assert_called_once_with("invalid-date-range")

    @patch('swagger_server.business.business.elaborate_workflows', return_value=[])
    @patch('swagger_server.business.business.elaborate_repository')
    @patch('swagger_server.business.business.validation.validate_date_range', return_value=None)
    def test_elaborate_statistic_success(self, mock_validate, mock_elaborate_repo, mock_elaborate_workflows):
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

        result = elaborate_statistic("repo/owner", "2023-01-01,2023-12-31")
        self.assertIsInstance(result, Statistics)

    @patch('swagger_server.business.business.validation.validate_date_range', return_value="Invalid range")
    def test_elaborate_statistic_invalid_date(self, mock_validate):
        with self.assertRaises(BadRequest):
            elaborate_statistic("helium/miner", "invalid-date")
        mock_validate.assert_called_once_with("invalid-date")

    @patch('swagger_server.business.business.elaborate_repositories')
    @patch('swagger_server.business.business.MongoOperations')
    def test_elaborate_metrics_repositories_success(self, MockMongoOperations, mock_repos):
        mock_repos.return_value.items = []
        result = elaborate_metrics_repositories()
        self.assertIsInstance(result, Metrics)


if __name__ == '__main__':
    unittest.main()
