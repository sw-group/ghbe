from swagger_server.models import RepositoriesList, Repository
from test import BaseTestCase
from test.fixtures import TEST_REPOSITORIES


class TestRepositoryController(BaseTestCase):
    """Tests for the GUI controller."""

    def setUp(self):
        """Set up test variables."""
        super().setUp()
        self.client = self.app.test_client()
        # Setup test data if needed
        self.mongo.db.repositories.insert_many(TEST_REPOSITORIES)

    def tearDown(self):
        """Tear down test variables."""
        super().tearDown()
        self.mongo.db.repositories.delete_many({})

    """Test the /repositories endpoint."""
    def test_get_repositories(self):
        """Test the /repositories endpoint without parameters."""
        response = self.client.get('/repositories')
        data = self.assert_json_response(response, 200)
        model = RepositoriesList.from_dict(data)  # convert dict to model

        self.assertIsInstance(model, RepositoriesList)
        self.assertEqual(len(model.items), len(TEST_REPOSITORIES))

    def test_get_repositories_with_pagination(self):
        """Test the /repositories endpoint with pagination parameters."""
        response = self.client.get('/repositories?page=1&size=2')
        data = self.assert_json_response(response, 200)
        model = RepositoriesList.from_dict(data)

        self.assertIsInstance(model, RepositoriesList)
        self.assertEqual(len(model.items), 2)

    def test_get_repositories_with_language_filter(self):
        """Test the /repositories endpoint with language filter."""
        language = 'Python'
        response = self.client.get(f'/repositories?language={language}')
        data = self.assert_json_response(response, 200)
        model = RepositoriesList.from_dict(data)

        self.assertIsInstance(model, RepositoriesList)
        for repo in model.items:
            self.assertEqual(repo.language, language)

    def test_get_repositories_with_no_matching_language(self):
        """Test the /repositories endpoint with a language that has no matches."""
        language = 'NonExistentLanguage'
        response = self.client.get(f'/repositories?language={language}')
        data = self.assert_json_response(response, 200)
        model = RepositoriesList.from_dict(data)

        self.assertIsInstance(model, RepositoriesList)
        self.assertEqual(len(model.items), 0)
        self.assertEqual(model.total_elements, None)

    def test_get_repositories_invalid_page(self):
        """Test the /repositories endpoint with a pagination less -1."""
        response = self.client.get('/repositories?page=-2')
        self.assert_json_response(response, 400)

    """ Edge test for /repositories endpoint with invalid parameters."""
    def test_get_repositories_invalid_parameters(self):
        response = self.client.get('/repositories?page=abc&size=-5')
        self.assert_json_response(response, 400)

    """ Other edge tests can be added similarly """
    def test_get_repositories_invalid_sort(self):
        response = self.client.get('/repositories?sort=invalid-sort-format')
        self.assert_json_response(response, 400)

    """Test the /repositories/{owner}/{name} endpoint."""
    def test_get_repository(self):
        repo_id = TEST_REPOSITORIES[0]['_id']

        response = self.client.get(f'/repositories/{repo_id}')
        data = self.assert_json_response(response, 200)
        model = Repository.from_dict(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(model.full_name, repo_id)

    def test_get_repository_not_found(self):
        response = self.client.get('/repositories/nonexistent_owner/nonexistent_repo')
        self.assert_json_response(response, 404)
