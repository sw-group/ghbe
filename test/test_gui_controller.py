from test import BaseTestCase
from test.fixtures import TEST_REPOSITORIES


class TestGuiController(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        # Setup test data if needed
        self.mongo.db.repositories.insert_many(TEST_REPOSITORIES)

    def tearDown(self):
        super().tearDown()
        self.mongo.db.repositories.delete_many({})

    def test_get_metrics(self):
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
