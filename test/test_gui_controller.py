from swagger_server.models import Metrics
from test import BaseTestCase
import swagger_server.db.database


class TestGuiController(BaseTestCase):
    """Tests for the GUI controller."""

    def setUp(self):
        """Set up test variables."""
        super().setUp()
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down test variables."""
        super().tearDown()
        swagger_server.db.database.mongo.db.repositories.delete_many({})

    def test_get_metrics(self):
        from test.fixtures import TEST_REPOSITORIES, LANGUAGES, MAXES
        # Setup test data
        swagger_server.db.database.mongo.db.repositories.insert_many(TEST_REPOSITORIES)

        """Test the /metrics endpoint."""
        response = self.client.get("/metrics")

        data = self.assert_json_response(response, 200)

        model = Metrics.from_dict(data)
        self.assertIsInstance(model, Metrics)

        # Check max counts
        self.assertEqual(MAXES, data["maxes"])
        # Check languages
        self.assertCountEqual(LANGUAGES, data["languages"])

    def test_get_metrics_no_data(self):
        """Test the /metrics endpoint with no data."""
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
