import unittest
from unittest.mock import patch, MagicMock
from swagger_server.controllers.gui_controller import get_metrics

"""Test the function `get_metrics` in isolation by mocking its dependencies (the business layer)."""

class TestGuiControllerUnit(unittest.TestCase):
    """UNIT TESTS - Test controller logic in isolation with mocks"""

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_success(self, mock_business):
        """Test successful metrics retrieval with mocked business layer"""
        # Arrange
        expected_response = {
            "languages": ["Python", "Java", "JavaScript"],
            "maxes": {
                "forks_count": 443,
                "stars_count": 3673
            }
        }

        mock_metrics = MagicMock()
        mock_metrics.to_dict.return_value = expected_response
        mock_business.elaborate_metrics_repositories.return_value = mock_metrics

        # Act
        result = get_metrics()

        # Assert
        mock_business.elaborate_metrics_repositories.assert_called_once()
        mock_metrics.to_dict.assert_called_once()
        self.assertEqual(result, expected_response)
        self.assertIsInstance(result, dict)

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_empty_data(self, mock_business):
        """Test metrics retrieval with empty data structure"""
        # Arrange
        mock_metrics = MagicMock()
        mock_metrics.to_dict.return_value = {"languages": [], "maxes": {}}
        mock_business.elaborate_metrics_repositories.return_value = mock_metrics

        # Act
        result = get_metrics()

        # Assert
        self.assertEqual(result["languages"], [])
        self.assertEqual(result["maxes"], {})

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_business_exception(self, mock_business):
        """Test exception handling when business layer fails"""
        # Arrange
        mock_business.elaborate_metrics_repositories.side_effect = Exception("Database unavailable")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_metrics()

        self.assertEqual(str(context.exception), "Database unavailable")

    @patch('swagger_server.controllers.gui_controller.business')
    def test_get_metrics_none_response(self, mock_business):
        """Test handling when business returns None"""
        # Arrange
        mock_business.elaborate_metrics_repositories.return_value = None

        # Act & Assert
        with self.assertRaises(AttributeError):
            get_metrics()

    def test_get_metrics_function_contract(self):
        """Test function signature and return type contract"""
        import inspect

        # Verify function takes no parameters
        sig = inspect.signature(get_metrics)
        self.assertEqual(len(sig.parameters), 0)

        # Verify function name
        self.assertEqual(get_metrics.__name__, 'get_metrics')