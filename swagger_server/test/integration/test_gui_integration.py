import unittest
from swagger_server.test import BaseTestCase


class TestGuiControllerIntegration(BaseTestCase):
    """Integration tests for /metrics endpoint"""

    def test_get_metrics_returns_json(self):
        """GET /metrics should return valid JSON"""
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("languages", data)
        self.assertIn("maxes", data)

    def test_get_metrics_languages_array(self):
        """GET /metrics should contain a languages array"""
        response = self.client.get("/metrics")
        data = self.assertJsonResponse(response, 200)

        self.assertIn("languages", data)
        self.assertIsInstance(data["languages"], list)

    def test_get_metrics_maxes_object(self):
        """GET /metrics should contain a maxes object with expected keys"""
        response = self.client.get("/metrics")
        data = self.assertJsonResponse(response, 200)

        self.assertIn("maxes", data)
        self.assertIsInstance(data["maxes"], dict)

        expected_keys = {
            "forks_count",
            "issue_count",
            "pr_count",
            "stars_count",
            "watchers_count",
            "workflows_count"
        }
        self.assertTrue(expected_keys.issubset(data["maxes"].keys()))

    def test_get_metrics_values_are_numbers(self):
        """Check that numeric fields in maxes are integers"""
        response = self.client.get("/metrics")
        data = self.assertJsonResponse(response, 200)

        for key, value in data["maxes"].items():
            self.assertIsInstance(value, int)


if __name__ == '__main__':
    unittest.main()
