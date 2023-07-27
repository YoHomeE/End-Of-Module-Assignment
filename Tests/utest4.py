import unittest
from unittest.mock import patch
from client import Client
from testdata import dict1, dict2, dict3, dict4, emptydict

class TestClient(unittest.TestCase):
    """Test cases for the Client class."""

    def setUp(self):
        """Set up the Client object before each test."""
        self.client = Client()

    @patch("builtins.input", side_effect=["name", "nicholas"])
    def test_createdict_single_dict(self, mock_input):
        """
        Test createdict method for a single dictionary.

        This test case mocks the user input and tests the createdict method of
        the Client class for creating a single dictionary. It provides the mock
        input 'name' and 'nicholas' and checks if the returned dictionary matches
        the expected dictionary.
        """
        num_members = 1
        num_keys = 1
        expected_dict = [{'name': 'nicholas'}]
        result = self.client.createdict(num_members, num_keys)
        self.assertEqual(result, expected_dict)

    @patch("builtins.input", side_effect=["hobby", "Surfing", "number", "10", "group", "b", "project", "server"])
    def test_createdict_multiple_dicts(self, mock_input):
        """
        Test createdict method for multiple dictionaries.

        This test case mocks the user input and tests the createdict method of
        the Client class for creating multiple dictionaries. It provides the mock
        input 'hobby', 'Surfing', 'number', '10', 'group', 'b', 'project', and
        'server', and checks if the returned list of dictionaries matches the
        expected list of dictionaries.
        """
        num_members = 2
        num_keys = 2  # Provide enough keys and values for two dictionaries with three pairs each
        expected_dict = [
            {'hobby': 'Surfing', 'number': '10'},
            {'group': 'b', 'project': 'server'}
        ]
        result = self.client.createdict(num_members, num_keys)
        self.assertEqual(result, expected_dict)

    def tearDown(self):
        """Clean up after each test by closing the client socket."""
        self.client.client.close()

if __name__ == '__main__':
    unittest.main()
