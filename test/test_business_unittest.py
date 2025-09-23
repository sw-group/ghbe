import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from werkzeug.exceptions import NotFound, BadRequest

from swagger_server.business.business import (
    elaborate_issues,
    elaborate_issue_comments,
    elaborate_repositories,
    elaborate_repository,
    elaborate_workflows,
    elaborate_statistics,
    elaborate_statistic,
    elaborate_metrics_repositories, elaborate_prs
)
from swagger_server.models import (
    IssuesList, CommentsList, RepositoriesList,
    Repository, Metrics, Statistics, Issue, Workflow
)

class TestElaborateFunctions(unittest.TestCase):

    @patch('swagger_server.business.business.mapper.map_response_to_issue')
    @patch('swagger_server.business.business.MongoOperations.count_issues')
    @patch('swagger_server.business.business.MongoOperations.get_issues')
    def test_elaborate_issues(self, mock_get_issues, mock_count_issues, mock_mapper):
        # Arrange
        mock_get_issues.return_value = [{"id": 1}]
        mock_count_issues.return_value = 1
        mock_mapper.return_value = {"mapped": "issue"}

        # Act
        result = elaborate_issues("repo/test", "OPEN", "2023-01-01,2023-12-31", 1)

        # Assert
        self.assertIsInstance(result, IssuesList)
        self.assertEqual(result.items, [{"mapped": "issue"}])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 1)

        mock_get_issues.assert_called_once_with(
            repo="repo/test",
            state="OPEN",
            date_range="2023-01-01,2023-12-31",
            page=1,
            sort=None
        )
        mock_count_issues.assert_called_once_with(
            repo="repo/test",
            state="OPEN",
            date_range="2023-01-01,2023-12-31"
        )
        mock_mapper.assert_called_once_with({"id": 1})

    @patch("swagger_server.business.business.mapper.map_response_to_issue")
    @patch("swagger_server.business.business.MongoOperations.count_prs")
    @patch("swagger_server.business.business.MongoOperations.get_prs")
    def test_elaborate_prs(self, mock_get_prs, mock_count_prs, mock_mapper):
        # Arrange
        mock_get_prs.return_value = [{"id": 1}]
        mock_count_prs.return_value = 1
        mock_mapper.return_value = {"mapped": "pr"}

        # Act
        result = elaborate_prs("repo/test", "OPEN", "2023-01-01,2023-12-31", 1)

        # Assert
        self.assertIsInstance(result, IssuesList)
        self.assertEqual(result.items, [{"mapped": "pr"}])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 1)

        mock_get_prs.assert_called_once_with(
            repo="repo/test",
            state="OPEN",
            date_range="2023-01-01,2023-12-31",
            page=1,
            sort=None,
        )
        mock_count_prs.assert_called_once_with(
            repo="repo/test",
            state="OPEN",
            date_range="2023-01-01,2023-12-31",
        )
        mock_mapper.assert_called_once_with({"id": 1})

    @patch("swagger_server.business.business.mapper.map_response_to_comment")
    @patch("swagger_server.business.business.MongoOperations.count_issue_comments")
    @patch("swagger_server.business.business.MongoOperations.get_comments")
    def test_elaborate_issue_comments(self, mock_get_comments, mock_count_comments, mock_mapper):
        # Arrange
        mock_get_comments.return_value = [{"comment": "hello"}]
        mock_count_comments.return_value = 1
        mock_mapper.return_value = {"mapped": "comment"}

        # Act
        result = elaborate_issue_comments("repo/test", 42, 1)

        # Assert
        self.assertIsInstance(result, CommentsList)
        self.assertEqual(result.items, [{"mapped": "comment"}])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 1)

        mock_get_comments.assert_called_once_with(
            repo="repo/test",
            number=42,
            page=1,
        )
        mock_count_comments.assert_called_once_with(
            repo="repo/test",
            number=42,
        )
        mock_mapper.assert_called_once_with({"comment": "hello"})

    @patch("swagger_server.business.business.mapper.map_response_to_repository")
    @patch("swagger_server.business.business.MongoOperations.count_repositories")
    @patch("swagger_server.business.business.MongoOperations.get_repositories")
    def test_elaborate_repositories(self, mock_get_repositories, mock_count_repositories, mock_mapper):
        # Arrange
        mock_get_repositories.return_value = [{"id": "r1"}]
        mock_count_repositories.return_value = 1
        mock_mapper.return_value = {"mapped": "repo"}

        # Act
        result = elaborate_repositories(name="test-repo", language="Python", page=1)

        # Assert
        self.assertIsInstance(result, RepositoriesList)
        self.assertEqual(result.items, [{"mapped": "repo"}])
        self.assertEqual(result.page, 1)
        self.assertEqual(result.total_elements, 1)

        mock_get_repositories.assert_called_once_with(
            name="test-repo",
            language="Python",
            is_private=None,
            date_range=None,
            stars=None,
            forks=None,
            issues=None,
            pulls=None,
            workflows=None,
            watchers=None,
            page=1,
            sort=None,
        )
        mock_count_repositories.assert_called_once_with(
            name="test-repo",
            language="Python",
            is_private=None,
            date_range=None,
            stars=None,
            forks=None,
            issues=None,
            pulls=None,
            workflows=None,
            watchers=None,
        )
        mock_mapper.assert_called_once_with({"id": "r1"})

class TestElaborateRepositoryAndStats(unittest.TestCase):

    @patch("swagger_server.business.business.mapper.map_response_to_repository")
    @patch("swagger_server.business.business.MongoOperations.get_repository")
    def test_elaborate_repository_success(self, mock_get_repository, mock_mapper):
        mock_get_repository.return_value = {"id": "r1"}
        mock_mapper.return_value = {"mapped": "repo"}

        result = elaborate_repository("repo/test")

        self.assertEqual(result, {"mapped": "repo"})
        mock_get_repository.assert_called_once_with("repo/test")
        mock_mapper.assert_called_once_with({"id": "r1"})

    @patch("swagger_server.business.business.MongoOperations.get_repository")
    def test_elaborate_repository_not_found(self, mock_get_repository):
        mock_get_repository.return_value = None

        with self.assertRaises(NotFound):
            elaborate_repository("repo/missing")

        mock_get_repository.assert_called_once_with("repo/missing")

    @patch("swagger_server.business.business.mapper.map_response_to_workflow")
    @patch("swagger_server.business.business.MongoOperations.get_workflows")
    @patch("swagger_server.business.business.MongoOperations.get_repository")
    def test_elaborate_workflows_success(self, mock_get_repository, mock_get_workflows, mock_mapper):
        mock_get_repository.return_value = {"id": "r1"}
        mock_get_workflows.return_value = {"workflows": [{"id": "wf1"}]}
        mock_mapper.return_value = {"mapped": "workflow"}

        result = elaborate_workflows("repo/test")

        self.assertEqual(result, [{"mapped": "workflow"}])
        mock_get_repository.assert_called_once_with("repo/test")
        mock_get_workflows.assert_called_once_with("repo/test")
        mock_mapper.assert_called_once_with({"id": "wf1"})

    @patch("swagger_server.business.business.MongoOperations.get_repository")
    def test_elaborate_workflows_not_found(self, mock_get_repository):
        mock_get_repository.return_value = None

        with self.assertRaises(NotFound):
            elaborate_workflows("repo/missing")

        mock_get_repository.assert_called_once_with("repo/missing")

    @patch("swagger_server.business.business.__compute_stats")
    @patch("swagger_server.business.business.elaborate_repositories")
    @patch("swagger_server.business.business.validation.validate_date_range")
    def test_elaborate_statistics_success(self, mock_validate, mock_elaborate_repositories, mock_compute):
        mock_validate.return_value = None
        mock_elaborate_repositories.return_value = RepositoriesList(items=[{"id": "r1"}], total_elements=1, page=1)
        mock_compute.return_value = "stats-result"

        result = elaborate_statistics("2023-01-01,2023-12-31", "repo", "Python", False, None, None, None, None,
                                      None, None, None)

        self.assertEqual(result, "stats-result")
        mock_validate.assert_called_once_with("2023-01-01,2023-12-31")
        mock_elaborate_repositories.assert_called_once()
        mock_compute.assert_called_once_with([{"id": "r1"}], "2023-01-01,2023-12-31")

    @patch("swagger_server.business.business.validation.validate_date_range")
    def test_elaborate_statistics_bad_request(self, mock_validate):
        mock_validate.return_value = "invalid-date"

        with self.assertRaises(BadRequest):
            elaborate_statistics("bad-date", None, None, None, None, None, None, None, None, None, None)

        mock_validate.assert_called_once_with("bad-date")

    @patch("swagger_server.business.business.__compute_stats")
    @patch("swagger_server.business.business.elaborate_repository")
    @patch("swagger_server.business.business.validation.validate_date_range")
    def test_elaborate_statistic_success(self, mock_validate, mock_elaborate_repository, mock_compute):
        mock_validate.return_value = None
        mock_elaborate_repository.return_value = {"id": "r1"}
        mock_compute.return_value = "stat-result"

        result = elaborate_statistic("repo/test", "2023-01-01,2023-12-31")

        self.assertEqual(result, "stat-result")
        mock_validate.assert_called_once_with("2023-01-01,2023-12-31")
        mock_elaborate_repository.assert_called_once_with("repo/test")
        mock_compute.assert_called_once_with([{"id": "r1"}], "2023-01-01,2023-12-31")

    @patch("swagger_server.business.business.validation.validate_date_range")
    def test_elaborate_statistic_bad_request(self, mock_validate):
        mock_validate.return_value = "invalid-date"

        with self.assertRaises(BadRequest):
            elaborate_statistic("repo/test", "bad-date")

        mock_validate.assert_called_once_with("bad-date")

    @patch("swagger_server.business.business.elaborate_repositories")
    def test_elaborate_metrics_repositories_success(self, mock_elaborate_repositories):
        # Mock repositories with .to_dict()
        repo1 = MagicMock()
        repo1.language = "Python"
        repo1.to_dict.return_value = {
            "stars_count": 5,
            "watchers_count": 3,
            "forks_count": 2,
            "issue_count": 1,
            "pr_count": 4,
            "workflows_count": 1,
        }
        repo2 = MagicMock()
        repo2.language = "Go"
        repo2.to_dict.return_value = {
            "stars_count": 10,
            "watchers_count": 8,
            "forks_count": 6,
            "issue_count": 3,
            "pr_count": 2,
            "workflows_count": 5,
        }
        mock_elaborate_repositories.return_value = RepositoriesList(items=[repo1, repo2], total_elements=2, page=-1)

        result = elaborate_metrics_repositories()

        self.assertIsInstance(result, Metrics)
        self.assertIn("Python", result.languages)
        self.assertIn("Go", result.languages)
        self.assertEqual(result.maxes["stars_count"], 10)
        self.assertEqual(result.maxes["watchers_count"], 8)
        self.assertEqual(result.maxes["forks_count"], 6)
        self.assertEqual(result.maxes["issue_count"], 3)
        self.assertEqual(result.maxes["pr_count"], 4)
        self.assertEqual(result.maxes["workflows_count"], 5)

        mock_elaborate_repositories.assert_called_once_with(page=-1)

class TestIntegrationComputeStats(unittest.TestCase):

    @patch("swagger_server.business.business.elaborate_issues")
    @patch("swagger_server.business.business.elaborate_prs")
    @patch("swagger_server.business.business.elaborate_workflows")
    @patch("swagger_server.business.business.elaborate_repository")
    @patch("swagger_server.business.business.validation.validate_date_range")
    def test_elaborate_statistic_integration(self, mock_validate, mock_elaborate_repository,
                                             mock_workflows, mock_prs, mock_issues):
        """
        Integration-style test for elaborate_statistic:
        - Runs __compute_stats and __get_stats logic.
        - Mocks only repository retrieval and data sources.
        - Adds created_at field to each issue/PR for util.generate_date_count_map.
        """

        # 1. Validation passes
        mock_validate.return_value = None

        # 2. Fake repository
        fake_repo = Repository(full_name="repo/test")
        mock_elaborate_repository.return_value = fake_repo

        # 3. Mock issues with created_at
        mock_issues.side_effect = lambda full_name, state, date_range, page: IssuesList(
            items=[Issue(
                title=f"issue-{state}",
                created_at=datetime(2023, 1, 1),
                body="Fix bug in code")],
            page=page,
            total_elements=1
        )

        # 4. Mock PRs with created_at
        mock_prs.side_effect = lambda full_name, state, date_range, page: IssuesList(
            items=[Issue(
                title=f"pr-{state}",
                created_at=datetime(2023, 1, 2),
                body="Add new feature")],
            page=page,
            total_elements=1
        )

        # 5. Mock workflows
        mock_workflows.return_value = [Workflow(id=1, name="wf1", lines=100, size="10 KB")]

        # Act
        result = elaborate_statistic("repo/test", "2023-01-01,2023-12-31")

        # Assert
        self.assertIsInstance(result, Statistics)
        self.assertIsInstance(result.issues, type(result.issues))
        self.assertIsInstance(result.pulls, type(result.pulls))
        self.assertIsInstance(result.workflows, type(result.workflows))
        self.assertIsInstance(result.repositories, type(result.repositories))

        # Validate mocks were called
        mock_validate.assert_called_once_with("2023-01-01,2023-12-31")
        mock_elaborate_repository.assert_called_once_with("repo/test")
        mock_issues.assert_any_call("repo/test", "OPEN", "2023-01-01,2023-12-31", -1)
        mock_issues.assert_any_call("repo/test", "CLOSED", "2023-01-01,2023-12-31", -1)
        mock_prs.assert_any_call("repo/test", "OPEN", "2023-01-01,2023-12-31", -1)
        mock_prs.assert_any_call("repo/test", "CLOSED", "2023-01-01,2023-12-31", -1)
        mock_prs.assert_any_call("repo/test", "MERGED", "2023-01-01,2023-12-31", -1)
        mock_workflows.assert_called_once_with("repo/test")

        # Check counts in the statistics
        self.assertEqual(result.pulls.merged, 1)
        self.assertIn("2023-01-01", result.issues.daily_opened_progress)
        self.assertIn("2023-01-02", result.pulls.daily_opened_progress)


if __name__ == '__main__':
    unittest.main()
