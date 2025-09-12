import unittest
from unittest.mock import patch

from swagger_server.controllers.gui_controller import get_metrics


# -------------------
# White Box Unit Tests
# -------------------
class TestGuiControllerWhiteBox(unittest.TestCase):
    """UNIT TESTS - White Box: know the internal business layer usage"""

    @patch('swagger_server.controllers.gui_controller.business.elaborate_metrics_repositories')
    def test_get_metrics_success(self, mock_elaborate):
        """Test successful metrics retrieval with mocked business layer"""
        expected_response = {
            "languages": ["Python", "Java", "JavaScript"],
            "maxes": {
                "forks_count": 443,
                "stars_count": 3673
            }
        }
        mock_elaborate.return_value.to_dict.return_value = expected_response

        result = get_metrics()

        mock_elaborate.assert_called_once()
        self.assertEqual(result, expected_response)
        self.assertIsInstance(result, dict)

    @patch('swagger_server.controllers.gui_controller.business.elaborate_metrics_repositories')
    def test_get_metrics_empty_data(self, mock_elaborate):
        """Test metrics retrieval with empty data structure"""
        mock_elaborate.return_value.to_dict.return_value = {"languages": [], "maxes": {}}

        result = get_metrics()

        self.assertEqual(result["languages"], [])
        self.assertEqual(result["maxes"], {})

    @patch('swagger_server.controllers.gui_controller.business.elaborate_metrics_repositories')
    def test_get_metrics_business_exception(self, mock_elaborate):
        """Test exception handling when business layer fails"""
        mock_elaborate.side_effect = Exception("Database unavailable")

        with self.assertRaises(Exception) as context:
            get_metrics()

        self.assertEqual(str(context.exception), "Database unavailable")

    @patch('swagger_server.controllers.gui_controller.business.elaborate_metrics_repositories')
    def test_get_metrics_none_response(self, mock_elaborate):
        """Test handling when business returns None"""
        mock_elaborate.return_value = None

        with self.assertRaises(AttributeError):
            get_metrics()


# -------------------
# Black Box Unit Tests
# -------------------
class TestGuiControllerBlackBox(unittest.TestCase):
    """UNIT TESTS - Black Box: function signature / contract verification"""

    def test_get_metrics_function_contract(self):
        """Test function signature and return type contract"""
        import inspect

        sig = inspect.signature(get_metrics)
        self.assertEqual(len(sig.parameters), 0)
        self.assertEqual(get_metrics.__name__, 'get_metrics')


if __name__ == '__main__':
    unittest.main()
