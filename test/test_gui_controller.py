from test import BaseTestCase
from test.fixtures import TEST_REPOSITORIES


class TestGuiController(BaseTestCase):
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

    def test_get_metrics(self):
        """Test the /metrics endpoint."""

        response = self.client.get("/metrics")
        data = self.assert_json_response(response, 200)

        # Check that languages are returned correctly
        self.assertIn("Python", data["languages"])
        self.assertIn("JavaScript", data["languages"])
        self.assertEqual(len(data["languages"]), 2)

        # Check max counts
        expected_maxes = {
            "stars_count": 20,
            "watchers_count": 10,
            "forks_count": 5,
            "issue_count": 3,
            "pr_count": 1,
            "workflows_count": 2
        }
        self.assertEqual(data["maxes"], expected_maxes)

    def test_get_metrics_no_data(self):
        """Test the /metrics endpoint with no data."""

        # Clear the database to simulate no data
        self.mongo.db.repositories.delete_many({})

        response = self.client.get("/metrics")
        data = self.assert_json_response(response, 200)

        # Check that languages are empty
        self.assertEqual(data["languages"], [])

        # Check max counts are zero
        expected_maxes = {
            "stars_count": 0,
            "watchers_count": 0,
            "forks_count": 0,
            "issue_count": 0,
            "pr_count": 0,
            "workflows_count": 0
        }
        self.assertEqual(data["maxes"], expected_maxes)
