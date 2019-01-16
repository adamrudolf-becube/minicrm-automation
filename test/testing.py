# users_test/test_users.py
import unittest
from users import get_users
from unittest.mock import patch
from command_handler import get_json_array_for_command


class BasicTests(unittest.TestCase):
    @patch('users.requests.get')  # Mock 'requests' module 'get' method.
    def test_request_response_with_decorator(self, mock_get):
        """Mocking using a decorator"""
        mock_get.return_value.status_code = 200 # Mock status code of response.
        response = get_users()

        # Assert that the request-response cycle completed successfully.
        self.assertEqual(response.status_code, 200)

    @patch('becube_crm_library.get_json_array_for_command')
    def test_test(self, mock_get):
        mock_get.return_value = "ASDF"

        eredmeny = get_json_array_for_command("Get students command")

        self.assertEqual(eredmeny, "ASDF")


if __name__ == "__main__":
    unittest.main()