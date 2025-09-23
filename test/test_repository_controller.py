from swagger_server.models import RepositoriesList, Repository, IssuesList, Workflow, CommentsList
from test import BaseTestCase
import swagger_server.db.database
from test.fixtures import TEST_ISSUES, TEST_PULLS, TEST_WORKFLOWS, TEST_COMMENTS


class TestRepositoryController(BaseTestCase):
    """Tests for the GUI controller."""

    def setUp(self):
        from test.fixtures import TEST_REPOSITORIES
        """Set up test variables."""
        super().setUp()
        self.client = self.app.test_client()
        # Setup test data if needed
        swagger_server.db.database.mongo.db.repositories.insert_many(TEST_REPOSITORIES)
        swagger_server.db.database.mongo.db.issues.insert_many(TEST_ISSUES)
        swagger_server.db.database.mongo.db.pullRequests.insert_many(TEST_PULLS)
        swagger_server.db.database.mongo.db.workflows.insert_many(TEST_WORKFLOWS)
        swagger_server.db.database.mongo.db.comments.insert_many(TEST_COMMENTS)

    def tearDown(self):
        """Tear down test variables."""
        super().tearDown()
        swagger_server.db.database.mongo.db.repositories.delete_many({})
        swagger_server.db.database.mongo.db.issues.delete_many({})
        swagger_server.db.database.mongo.db.pullRequests.delete_many({})
        swagger_server.db.database.mongo.db.workflows.delete_many({})
        swagger_server.db.database.mongo.db.comments.delete_many({})

    """Test the /repositories endpoint."""
    def test_get_repositories(self):
        """Test the /repositories endpoint without parameters."""
        response = self.client.get('/repositories')

        data = self.assert_json_response(response, 200)

        model = RepositoriesList.from_dict(data)  # convert dict to model
        self.assertIsInstance(model, RepositoriesList)
        self.assertEqual(model.total_elements, 20)

    def test_get_repositories_with_pagination(self):
        """Test the /repositories endpoint with pagination parameters."""
        response = self.client.get('/repositories?page=2')

        data = self.assert_json_response(response, 200)

        model = RepositoriesList.from_dict(data)
        self.assertIsInstance(model, RepositoriesList)
        self.assertEquals(model.items, [])
        self.assertEqual(model.total_elements, 20)

    def test_get_repositories_with_language_filter(self):
        """Test the /repositories endpoint with language filter."""
        response = self.client.get(f'/repositories?language=Python')

        data = self.assert_json_response(response, 200)

        model = RepositoriesList.from_dict(data)
        self.assertIsInstance(model, RepositoriesList)
        for repo in model.items:
            self.assertEqual(repo.language, 'Python')
        self.assertEqual(model.total_elements, 2)

    def test_get_repositories_with_no_matching_language(self):
        """Test the /repositories endpoint with a language that has no matches."""
        language = 'NonExistentLanguage'
        response = self.client.get(f'/repositories?language={language}')

        data = self.assert_json_response(response, 200)

        model = RepositoriesList.from_dict(data)
        self.assertIsInstance(model, RepositoriesList)
        self.assertEqual(model.total_elements, 0)

    def test_get_repositories_invalid_page(self):
        """Test the /repositories endpoint with a pagination less -1."""
        response = self.client.get('/repositories?page=-2')
        self.assert_json_response(response, 400)

    def test_get_repositories_invalid_parameters(self):
        """ Edge test for /repositories endpoint with invalid parameters."""
        response = self.client.get('/repositories?page=abc')
        self.assert_json_response(response, 400)

    def test_get_repositories_invalid_sort(self):
        """ Edge test for /repositories endpoint with invalid sort format."""
        response = self.client.get('/repositories?sort=invalid-sort-format')
        self.assert_json_response(response, 400)

    """Test the /repositories/{owner}/{name} endpoint."""
    def test_get_repository(self):
        """Test the /repositories/{owner}/{name} endpoint with a valid repository."""
        repo_id = 'user/repo1'

        response = self.client.get(f'/repositories/{repo_id}')

        data = self.assert_json_response(response, 200)

        model = Repository.from_dict(data)
        self.assertEqual(model.full_name, repo_id)

    def test_get_repository_not_found(self):
        """ Test the /repositories/{owner}/{name} endpoint with a non-existent repository."""
        response = self.client.get('/repositories/nonexistent_owner/nonexistent_repo')
        self.assert_json_response(response, 404)

    """Test the /repositories/{owner}/{name}/issues endpoint."""
    def test_get_repository_issues(self):
        """Test the /repositories/{owner}/{name}/issues endpoint with a valid repository."""
        repo_id = 'user/repo1'

        response = self.client.get(f'/repositories/{repo_id}/issues?issue_type=issues')

        data = self.assert_json_response(response, 200)

        model = IssuesList.from_dict(data)
        self.assertIsInstance(model, IssuesList)
        self.assertEquals(model.total_elements, 2)

    def test_get_repository_issue_with_sort(self):
        """Test the /repositories/{owner}/{name}/issues endpoint with a valid repository and sort parameter."""
        repo_id = 'user/repo1'

        response = self.client.get(f'/repositories/{repo_id}/issues?issue_type=issues&sort=createdAt-desc')

        data = self.assert_json_response(response, 200)

        model = IssuesList.from_dict(data)
        self.assertIsInstance(model, IssuesList)
        self.assertEquals(model.total_elements, 2)
        self.assertLessEqual(model.items[1].created_at, model.items[0].created_at)

    def test_get_repository_no_exist_issues(self):
        """ Test the /repositories/{owner}/{name}/issues endpoint with a non-existent repository."""
        response = self.client.get('/repositories/nonexistent_owner/nonexistent_repo/issues?issue_type=issues')
        data = self.assert_json_response(response, 200)

        model = IssuesList.from_dict(data)
        self.assertIsInstance(model, IssuesList)
        self.assertEquals(model.total_elements, 0)

    def test_get_repository_pulls(self):
        """Test the /repositories/{owner}/{name}/issues endpoint with a valid repository."""
        repo_id = 'user/repo1'

        response = self.client.get(f'/repositories/{repo_id}/issues?issue_type=pulls')

        data = self.assert_json_response(response, 200)

        model = IssuesList.from_dict(data)
        self.assertIsInstance(model, IssuesList)
        self.assertEquals(model.total_elements, 2)

    def test_get_repository_no_exist_pulls(self):
        """ Test the /repositories/{owner}/{name}/pulls endpoint with a non-existent repository."""
        response = self.client.get('/repositories/nonexistent_owner/nonexistent_repo/issues?issue_type=pulls')
        data = self.assert_json_response(response, 200)

        model = IssuesList.from_dict(data)
        self.assertIsInstance(model, IssuesList)
        self.assertEquals(model.total_elements, 0)

    def test_get_repository_issues_invalid_issue_type(self):
        """ Edge test for /repositories/{owner}/{name}/issues endpoint with invalid issue_type."""
        repo_id = 'user/repo1'
        response = self.client.get(f'/repositories/{repo_id}/issues?issue_type=invalid_type')
        self.assert_json_response(response, 400)

    def test_get_repository_issues_invalid_page(self):
        """ Edge test for /repositories/{owner}/{name}/issues endpoint with invalid page."""
        repo_id = 'user/repo1'
        response = self.client.get(f'/repositories/{repo_id}/issues?page=-1&issue_type=issues')
        self.assert_json_response(response, 400)

    def test_get_repository_issues_without_issue_type(self):
        """ Edge test for /repositories/{owner}/{name}/issues endpoint without issue_type."""
        repo_id = 'user/repo1'
        response = self.client.get(f'/repositories/{repo_id}/issues')
        self.assert_json_response(response, 400)

    def test_get_repository_issues_invalid_sort(self):
        """ Edge test for /repositories/{owner}/{name}/issues endpoint with invalid sort format."""
        repo_id = 'user/repo1'
        response = self.client.get(f'/repositories/{repo_id}/issues?issue_type=issues&sort=invalid-sort-format')
        self.assert_json_response(response, 400)

    """Test the /repositories/{owner}/{name}/issues/{number}/comments endpoint."""
    def test_get_repository_issue_comments(self):
        """Test the /repositories/{owner}/{name}/issues/{number}/comments endpoint with a valid issue."""
        repo_id = 'user/repo1'
        issue_number = 1001

        response = self.client.get(f'/repositories/{repo_id}/issues/{issue_number}/comments')

        data = self.assert_json_response(response, 200)

        model = CommentsList.from_dict(data)
        self.assertIsInstance(model, CommentsList)
        self.assertEqual(model.total_elements, 2)
        for comment in model.items:
            self.assertTrue(hasattr(comment, 'author'))
            self.assertTrue(hasattr(comment, 'message'))
            self.assertTrue(hasattr(comment, 'created_at'))
            self.assertTrue(hasattr(comment, 'updated_at'))
            self.assertTrue(hasattr(comment, 'association'))

    def test_get_repository_issue_no_exist_comments(self):
        """ Test the /repositories/{owner}/{name}/issues/{number}/comments endpoint with a non-existent issue."""
        repo_id = 'user/repo1'
        issue_number = 9999

        response = self.client.get(f'/repositories/{repo_id}/issues/{issue_number}/comments')

        data = self.assert_json_response(response, 200)

        model = CommentsList.from_dict(data)
        self.assertIsInstance(model, CommentsList)
        self.assertEquals(model.total_elements, 0)


    """Test the /repositories/{owner}/{name}/workflow endpoint."""
    def test_get_repository_workflow(self):
        """Test the /repositories/{owner}/{name}/workflow endpoint with a valid repository."""
        repo_id = 'user/repo1'
        response = self.client.get(f'/repositories/{repo_id}/workflows')

        data = self.assert_json_response(response, 200)

        models = [Workflow.from_dict(item) for item in data]
        self.assertEqual(len(models), 2)
        # Check that all elements are Workflow instances
        for m in models:
            self.assertIsInstance(m, Workflow)
            self.assertTrue(hasattr(m, 'id'))
            self.assertTrue(hasattr(m, 'name'))
            self.assertTrue(hasattr(m, 'created_at'))
            self.assertTrue(hasattr(m, 'updated_at'))
            self.assertTrue(hasattr(m, 'url'))
            self.assertTrue(hasattr(m, 'file_url'))
            self.assertTrue(hasattr(m, 'path'))
            self.assertTrue(hasattr(m, 'size'))
            self.assertTrue(hasattr(m, 'lines'))
            self.assertTrue(hasattr(m, 'state'))

    def test_get_repository_no_exist_workflow(self):
        """ Test the /repositories/{owner}/{name}/workflow endpoint with a non-existent repository."""
        response = self.client.get('/repositories/nonexistent_owner/nonexistent_repo/workflows')
        self.assert_json_response(response, 404)


