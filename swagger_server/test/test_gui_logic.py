import unittest
from swagger_server.business.business import elaborate_metrics_repositories


class TestGuiControllerBusinessLogic(unittest.TestCase):
    """BUSINESS LOGIC TESTS - Test actual business implementation"""

    def test_elaborate_metrics_repositories_real(self):
        """Test the real business logic implementation"""
        # Act
        result = elaborate_metrics_repositories()

        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'to_dict'))

        metrics_dict = result.to_dict()

        # Verify structure
        self.assertIn("languages", metrics_dict)
        self.assertIn("maxes", metrics_dict)
        self.assertIsInstance(metrics_dict["languages"], list)
        self.assertIsInstance(metrics_dict["maxes"], dict)

        # Verify maxes contains expected keys
        expected_max_keys = {
            "forks_count", "issue_count", "pr_count",
            "stars_count", "watchers_count", "workflows_count"
        }
        self.assertEqual(set(metrics_dict["maxes"].keys()), expected_max_keys)

        # Verify data types
        for key in metrics_dict["maxes"]:
            self.assertIsInstance(metrics_dict["maxes"][key], (int, float))

    def test_elaborate_metrics_languages_content(self):
        """Test that languages list contains expected values"""
        # Act
        result = elaborate_metrics_repositories()
        metrics_dict = result.to_dict()

        # Assert
        self.assertIsInstance(metrics_dict["languages"], list)

        # Verify we have some programming languages
        expected_languages = ["Python", "Java", "JavaScript", "C++", "HTML"]
        for lang in expected_languages:
            self.assertIn(lang, metrics_dict["languages"])