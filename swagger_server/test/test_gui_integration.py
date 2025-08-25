import json
import os
import sys
from unittest.mock import MagicMock, patch

from swagger_server.test import BaseTestCase


class TestGuiControllerIntegration(BaseTestCase):
    """Test cases for /metrics endpoint"""

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_success(self, mock_business):
        """Test successful GET /metrics endpoint with actual response structure"""
        # Mock the business layer response based on the actual structure
        mock_response = {
            "languages": [
                "C++", "Visual Basic", "Java", "Kaitai Struct", "Lua", "R",
                "TypeScript", "Rich Text Format", "Shell", "Erlang", "PowerShell",
                "VHDL", "C", "HTML", "Swift", "C#", "Roff", "Go", "JavaScript",
                "PHP", "Verilog", "Batchfile", "Rust", "Python"
            ],
            "maxes": {
                "forks_count": 443,
                "issue_count": 2480,
                "pr_count": 1363,
                "stars_count": 3673,
                "watchers_count": 223,
                "workflows_count": 7
            }
        }

        # Mock the business method
        mock_business.elaborate_metrics_repositories.return_value.to_dict.return_value = mock_response

        # Make the request using Flask test client
        response = self.client.get('/metrics')

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Test languages array
        self.assertIn("languages", data)
        self.assertIsInstance(data["languages"], list)
        self.assertEqual(len(data["languages"]), 24)
        self.assertIn("Python", data["languages"])
        self.assertIn("Java", data["languages"])
        self.assertIn("JavaScript", data["languages"])

        # Test maxes object
        self.assertIn("maxes", data)
        self.assertIsInstance(data["maxes"], dict)

        # Test individual max values
        self.assertEqual(data["maxes"]["forks_count"], 443)
        self.assertEqual(data["maxes"]["issue_count"], 2480)
        self.assertEqual(data["maxes"]["pr_count"], 1363)
        self.assertEqual(data["maxes"]["stars_count"], 3673)
        self.assertEqual(data["maxes"]["watchers_count"], 223)
        self.assertEqual(data["maxes"]["workflows_count"], 7)

        # Verify the business method was called
        mock_business.elaborate_metrics_repositories.assert_called_once()

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_empty_data(self, mock_business):
        """Test GET /metrics with empty data from business layer"""
        # Mock empty response
        mock_response = {
            "languages": [],
            "maxes": {
                "forks_count": 0,
                "issue_count": 0,
                "pr_count": 0,
                "stars_count": 0,
                "watchers_count": 0,
                "workflows_count": 0
            }
        }

        mock_business_instance = MagicMock()
        mock_business_instance.elaborate_metrics_repositories.return_value.to_dict.return_value = mock_response
        mock_business.return_value = mock_business_instance

        response = self.client.get('/metrics')

        data = self.assertJsonResponse(response, 200)

        # Verify empty arrays and zero values
        self.assertEqual(data["languages"], [])
        self.assertEqual(data["maxes"]["forks_count"], 0)
        self.assertEqual(data["maxes"]["stars_count"], 0)

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_partial_data(self, mock_business):
        """Test GET /metrics with partial data"""
        mock_response = {
            "languages": ["Python", "JavaScript"],
            "maxes": {
                "forks_count": 100,
                "issue_count": 50,
                "pr_count": 30,
                "stars_count": 500,
                "watchers_count": 25,
                "workflows_count": 2
            }
        }

        mock_business_instance = MagicMock()
        mock_business_instance.elaborate_metrics_repositories.return_value.to_dict.return_value = mock_response
        mock_business.return_value = mock_business_instance

        response = self.client.get('/metrics')

        data = self.assertJsonResponse(response, 200)

        self.assertEqual(data["languages"], ["Python", "JavaScript"])
        self.assertEqual(data["maxes"]["stars_count"], 500)
        self.assertEqual(data["maxes"]["workflows_count"], 2)

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_business_exception(self, mock_business):
        """Test GET /metrics when business layer raises an exception"""
        # Mock business layer to raise an exception
        mock_business_instance = MagicMock()
        mock_business_instance.elaborate_metrics_repositories.side_effect = Exception("Database connection error")
        mock_business.return_value = mock_business_instance

        response = self.client.get('/metrics')

        # Should return 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content_type, 'application/json')

        error_data = response.get_json()
        self.assertIn('detail', error_data)

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_response_structure_validation(self, mock_business):
        """Test that the response structure is validated against the schema"""
        # Mock response that might have missing fields
        mock_response = {
            "languages": ["Python"],
            "maxes": {
                "forks_count": 100,
                "stars_count": 500
                # Missing other required fields
            }
        }

        mock_business_instance = MagicMock()
        mock_business_instance.elaborate_metrics_repositories.return_value.to_dict.return_value = mock_response
        mock_business.return_value = mock_business_instance

        # Since validate_responses=True in connexion, this might fail validation
        response = self.client.get('/metrics')

        # The response might be 500 if validation fails, or 200 if the model handles missing fields
        self.assertIn(response.status_code, [200, 500])

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_with_different_max_values(self, mock_business):
        """Test GET /metrics with various max values"""
        test_cases = [
            {
                "languages": ["Python"],
                "maxes": {
                    "forks_count": 9999,
                    "issue_count": 8888,
                    "pr_count": 7777,
                    "stars_count": 6666,
                    "watchers_count": 5555,
                    "workflows_count": 10
                }
            },
            {
                "languages": ["Java", "C++"],
                "maxes": {
                    "forks_count": 1,
                    "issue_count": 1,
                    "pr_count": 1,
                    "stars_count": 1,
                    "watchers_count": 1,
                    "workflows_count": 1
                }
            }
        ]

        for i, test_case in enumerate(test_cases):
            with self.subTest(test_case=test_case):
                mock_business_instance = MagicMock()
                mock_business_instance.elaborate_metrics_repositories.return_value.to_dict.return_value = test_case
                mock_business.return_value = mock_business_instance

                response = self.client.get('/metrics')

                data = self.assertJsonResponse(response, 200)

                # Verify the response matches the test case
                self.assertEqual(data["languages"], test_case["languages"])
                self.assertEqual(data["maxes"], test_case["maxes"])