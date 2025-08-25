import unittest
from swagger_server.test import BaseTestCase
from swagger_server.business.business import elaborate_metrics_repositories

"""
    Test the entire stack, including the business layer and possibly the database or other services,
    but typically without mocking the business layer. However, for E2E tests, 
    we might use a test database or mock external services.
"""

class TestGuiControllerEndToEnd(BaseTestCase):
    """END-TO-END TESTS - Test complete flow with real business logic"""

    def test_get_metrics_end_to_end(self):
        """Test complete flow from HTTP request to real business response"""
        # Act
        response = self.client.get('/metrics')

        # Assert HTTP response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = response.json

        # Verify response structure
        self.assertIn("languages", data)
        self.assertIn("maxes", data)
        self.assertIsInstance(data["languages"], list)
        self.assertIsInstance(data["maxes"], dict)

        # Verify consistency with direct business call
        direct_result = elaborate_metrics_repositories().to_dict()
        self.assertEqual(data, direct_result)

    def test_metrics_data_consistency(self):
        """Test that metrics data is consistent across multiple calls"""
        # First call
        response1 = self.client.get('/metrics')
        data1 = response1.json

        # Second call
        response2 = self.client.get('/metrics')
        data2 = response2.json

        # Should be identical (unless underlying data changed rapidly)
        self.assertEqual(data1, data2)

        # Verify specific data integrity
        self.assertGreater(len(data1["languages"]), 0)
        self.assertGreater(data1["maxes"]["stars_count"], 0)

    def test_metrics_completeness(self):
        """Test that all expected metrics fields are present with valid data"""
        response = self.client.get('/metrics')
        data = response.json

        # Verify all expected maxes fields are present
        required_max_fields = [
            "forks_count", "issue_count", "pr_count",
            "stars_count", "watchers_count", "workflows_count"
        ]

        for field in required_max_fields:
            self.assertIn(field, data["maxes"])
            self.assertIsInstance(data["maxes"][field], (int, float))
            self.assertGreaterEqual(data["maxes"][field], 0)

        # Verify languages list is populated
        self.assertGreater(len(data["languages"]), 0)
        self.assertIsInstance(data["languages"][0], str)