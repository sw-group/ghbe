import unittest
from swagger_server.test import BaseTestCase
from swagger_server.business.business import elaborate_metrics_repositories

class TestGuiControllerEndToEnd(BaseTestCase):
    """END-TO-END TESTS - Full stack including business layer"""

    def test_get_metrics_end_to_end(self):
        """Test complete flow from HTTP request to real business response"""
        response = self.client.get('/metrics')

        # Assert HTTP response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("languages", data)
        self.assertIn("maxes", data)

        # Verify consistency with direct business call
        direct_result = elaborate_metrics_repositories().to_dict()
        # Compare languages ignoring order
        self.assertCountEqual(data["languages"], direct_result["languages"])
        # Compare maxes exactly
        self.assertEqual(data["maxes"], direct_result["maxes"])

    def test_metrics_data_consistency(self):
        """Test that metrics data is consistent across multiple calls"""
        data1 = self.client.get('/metrics').get_json()
        data2 = self.client.get('/metrics').get_json()

        self.assertCountEqual(data1["languages"], data2["languages"])
        self.assertEqual(data1["maxes"], data2["maxes"])

        # Verify basic data integrity
        self.assertGreater(len(data1["languages"]), 0)
        self.assertGreaterEqual(data1["maxes"]["stars_count"], 0)

    def test_metrics_completeness(self):
        """Test that all expected metrics fields are present with valid data"""
        data = self.client.get('/metrics').get_json()

        required_max_fields = [
            "forks_count", "issue_count", "pr_count",
            "stars_count", "watchers_count", "workflows_count"
        ]

        for field in required_max_fields:
            self.assertIn(field, data["maxes"])
            self.assertIsInstance(data["maxes"][field], (int, float))
            self.assertGreaterEqual(data["maxes"][field], 0)

        # Languages list checks
        self.assertGreater(len(data["languages"]), 0)
        self.assertIsInstance(data["languages"][0], str)


if __name__ == '__main__':
    unittest.main()
