import unittest
from unittest.mock import patch, MagicMock

from swagger_server.controllers import repository_controller as rc


class TestRepositoryControllerWhiteBox(unittest.TestCase):

    @patch('swagger_server.controllers.repository_controller.business.elaborate_workflows')
    def test_get_workflows_of_repo_returns_list_of_dicts(self, mock_elaborate):
        """Test get_workflows_of_repo to cover the list comprehension"""
        # Create a mock workflow with to_dict()
        mock_workflow = MagicMock()
        mock_workflow.to_dict.return_value = {'id': 1, 'name': 'CI Pipeline'}
        mock_elaborate.return_value = [mock_workflow]

        result = rc.get_workflows_of_repo('owner_example', 'repo_example')

        # Assert the result is a list of dicts
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['name'], 'CI Pipeline')

        # Ensure the mocks to_dict() was called
        mock_workflow.to_dict.assert_called_once()


if __name__ == '__main__':
    unittest.main()
